import asyncio
import io
import random
from queue import Queue
from typing import Literal

import discord
from discord.ext import commands
from discord import app_commands

from ..generator_api import BaseGeneratorApi, ComfyUI
from ..config import configuration


class ImagineCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue: Queue = Queue()
        self.generator: BaseGeneratorApi = ComfyUI()
        self.bot.loop.create_task(self.queue_worker())

    @app_commands.command(name="imagine")
    async def imagine(
            self,
            i: discord.Interaction,
            positive_prompt: str,
            negative_prompt: str = '',
            aspect_ratio: Literal['1:1', '2:3', '3:2', '16:9', '9:16'] = '2:3',
            seed: int | None = None
    ):
        r: discord.InteractionResponse = i.response
        try:
            await r.defer()
        except discord.errors.HTTPException:
            return

        seed = seed or random.randint(0, 100000000)

        if aspect_ratio not in configuration.generation_sizes:
            await i.edit_original_response(
                content="Niepoprawna konfiguracja pluginu imagine - brak wymiarów dla podanego aspect ratio")
            return

        width, height = configuration.generation_sizes[aspect_ratio]

        prompt_id = self.generator.queue_prompt(
            positive_prompt,
            negative_prompt,
            width,
            height,
            seed
        )
        self.queue.put((i, prompt_id, seed))

    async def queue_worker(self):
        while True:
            if self.queue.empty():
                await asyncio.sleep(1)
                continue

            i, prompt_id, seed = self.queue.get()
            if not self.generator.is_ready(prompt_id):
                self.queue.put((i, prompt_id, seed))
                continue

            images: list[bytes] = self.generator.get_result(prompt_id)
            if not images:
                await i.edit_original_response(content="Wygląda na to, że coś poszło nie tak i niczego nie wygenerowano")
                continue

            await i.edit_original_response(content=f"`seed: {seed}`", attachments=[
                discord.File(io.BytesIO(image), filename=f"image_{i}.png") for i, image in enumerate(images)
            ])
