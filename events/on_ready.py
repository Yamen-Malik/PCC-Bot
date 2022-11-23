from discord.ext import commands


@commands.Cog.listener()
async def on_ready():
    print(f"Running")

exported_events = [on_ready]
