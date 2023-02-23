from discord.ext import commands
from logging import getLogger

@commands.Cog.listener()
async def on_ready():
    getLogger(__name__).info("Running...")

exported_events = [on_ready]
