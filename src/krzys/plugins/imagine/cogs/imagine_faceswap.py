import asyncio
import io
from queue import Queue

import discord
from discord.ext import commands
from discord import app_commands

from .. import config
from ..generator_api import BaseGeneratorApi, ComfyUI
from krzys.plugins.face_swap.face_swap import get_one_face, process_image


class ImagineFaceSwapCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue: Queue = Queue()
        self.generator: BaseGeneratorApi = ComfyUI()
        self.bot.loop.create_task(self.queue_worker())

    @app_commands.command(name="imagine_faceswap")
    async def imagine_faceswap(
            self,
            i: discord.Interaction,
            source_face: discord.Attachment,
            positive_prompt: str,
            negative_prompt: str = ''
    ):
        r: discord.InteractionResponse = i.response
        try:
            await r.defer()
        except discord.errors.HTTPException:
            return

        source_face = await source_face.read()
        source_face = get_one_face(source_face)
        if source_face is None:
            await i.edit_original_response(content="Nie udało się znaleźć twarzy na zdjęciu")
            return

        prompt_id = self.generator.queue_prompt(positive_prompt, negative_prompt, 1024, 1024, seed=0)
        self.queue.put((source_face, i, prompt_id))

    async def queue_worker(self):
        while True:
            if self.queue.empty():
                await asyncio.sleep(1)
                continue

            source, i, prompt_id = self.queue.get()
            if not self.generator.is_ready(prompt_id):
                self.queue.put((source, i, prompt_id))
                continue

            images: list[bytes] = self.generator.get_result(prompt_id)
            if not images:
                await i.edit_original_response(content="Wygląda na to, że coś poszło nie tak i niczego nie wygenerowano")
                continue

            swapped_images = []
            for image in images:
                try:
                    swapped_images.append(process_image(source, image))
                except Exception:
                    swapped_images.append(image)

            await i.edit_original_response(content="Patrz co namalowałem", attachments=[
                discord.File(io.BytesIO(image), filename=f"image_{i}.png") for i, image in enumerate(swapped_images)
            ])
