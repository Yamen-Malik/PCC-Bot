from discord.ext import commands
from discord import Guild
from replit import db
from constants import DEFAULT_GUILD_DATA
from copy import deepcopy
from logging import getLogger

@commands.Cog.listener()
async def on_guild_join(guild: Guild):
    getLogger(__name__).info(f"Joined new guild. Guild({guild.name}, {guild.id})")
    db[str(guild.id)] = deepcopy(DEFAULT_GUILD_DATA)    

exported_events = [on_guild_join]
