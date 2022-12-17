from discord.ext import commands
from discord import Guild
from replit import db
from constants import DEFAULT_GUILD_DATA


@commands.Cog.listener()
async def on_guild_join(guild: Guild):
    db[str(guild.id)] = DEFAULT_GUILD_DATA

exported_events = [on_guild_join]
