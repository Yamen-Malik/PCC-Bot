from discord.ext import commands

@commands.Cog.listener()
async def on_ready():
    print("Running...")

exported_events = [on_ready]
