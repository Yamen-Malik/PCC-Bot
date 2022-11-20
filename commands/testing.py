from discord.ext import commands
from commands.decorators import command
from events.on_member_join import on_member_join


@commands.command(name="welcome", help="welcome a member to the server (used to test on_member_join)")
@command
async def welcome(ctx):
    await on_member_join(ctx.author)
