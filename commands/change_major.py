from discord.ext import commands
from commands.decorators import command
from major_menu import MajorMenu


@commands.command(name="change_major", help="Change your major role")
@command
async def change_major(ctx):
    menu = MajorMenu(None)
    await ctx.send("Choose major:", view=menu)
