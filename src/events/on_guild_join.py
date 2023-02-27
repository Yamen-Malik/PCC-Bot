from copy import deepcopy
from logging import getLogger

from discord.ext.commands import Cog, Bot
from discord import Guild
from replit import db

from constants import DEFAULT_GUILD_DATA


class OnGuildJoin(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = getLogger(__name__)

    @Cog.listener()
    async def on_guild_join(self, guild: Guild):
        self.logger.info(f"Joined new guild. Guild({guild.name}, {guild.id})")
        db[str(guild.id)] = deepcopy(DEFAULT_GUILD_DATA)

        self.logger("Syncing app commands globally.")
        self.bot.tree.sync()


async def setup(bot: Bot) -> None:
    await bot.add_cog(OnGuildJoin(bot))
