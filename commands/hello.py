from discord.ext import commands
from utilities.decorators import command


@commands.command(name="hello", help="Say hello to the bot")
@command
async def hello(ctx):
    await ctx.send("Hi.")
