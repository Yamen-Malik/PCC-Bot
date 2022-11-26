from discord.ext import commands
from replit import db
from constants import DEFAULT_GUILD_DATA


@commands.Cog.listener()
async def on_guild_join(guild):
    db[guild.id] = DEFAULT_GUILD_DATA.copy()

exported_events = [on_guild_join]
