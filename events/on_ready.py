from discord.ext.commands import Cog, Bot
from logging import getLogger

class OnReady(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = getLogger(__name__)
        
    @Cog.listener()
    async def on_ready(self):
        self.logger.info("Running...")

                


async def setup(bot: Bot) -> None:
    await bot.add_cog(OnReady(bot))
