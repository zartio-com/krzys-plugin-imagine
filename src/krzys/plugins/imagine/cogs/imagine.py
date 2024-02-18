import asyncio
import io
from queue import Queue

import discord
from discord.ext import commands
from discord import app_commands

from .. import config
from ..generator_api import BaseGeneratorApi, ComfyUI


class ImagineCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue: Queue = Queue()
        self.generator: BaseGeneratorApi = ComfyUI()
        self.bot.loop.create_task(self.queue_worker())

    @app_commands.command(name="imagine")
    async def imagine(self, i: discord.Interaction, positive_prompt: str, negative_prompt: str = ''):
        r: discord.InteractionResponse = i.response
        try:
            await r.defer()
        except discord.errors.HTTPException:
            return

        prompt_id = self.generator.queue_prompt(positive_prompt, negative_prompt)
        self.queue.put((i, prompt_id))

    async def queue_worker(self):
        while True:
            if self.queue.empty():
                await asyncio.sleep(1)
                continue

            i, prompt_id = self.queue.get()
            if not self.generator.is_ready(prompt_id):
                self.queue.put((i, prompt_id))
                continue

            images: list[bytes] = self.generator.get_result(prompt_id)
            if not images:
                await i.edit_original_response(content="Wygląda na to, że coś poszło nie tak i niczego nie wygenerowano")
                continue

            await i.edit_original_response(content="Patrz co namalowałem", attachments=[
                discord.File(io.BytesIO(image), filename=f"image_{i}.png") for i, image in enumerate(images)
            ])
