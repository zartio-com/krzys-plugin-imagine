import krzys.core
from . import cogs


class Plugin(krzys.core.Plugin):
    async def load(self):
        await self.bot.add_cog(cogs.ImagineCog(self.bot))

        try:
            import krzys.plugins.face_swap
            await self.bot.add_cog(cogs.ImagineFaceSwapCog(self.bot))
        except ImportError:
            pass
