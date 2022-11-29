from discord.ext import commands
from utils.decorators import command


@commands.command(name="hello", help="Say hello to the bot")
@command
async def hello(ctx: commands.Context) -> bool:
    await ctx.send(f"Hi {ctx.author.mention}.")
    return True

exported_commands = [hello]
