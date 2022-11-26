from discord.ext import commands
from discord import ButtonStyle
from utils.choose_role import choose_role
from utils.decorators import command
from utils.menu import create_menu
from replit import db


@commands.command(name="change_role", help="Change your member role")
@command
async def change_role(ctx: commands.Context):
    if db[ctx.guild.id]["new_member_roles"] < 2:
        return

    menu = create_menu(
        db[ctx.guild.id]["new_member_roles"],
        [choose_role],
        [ButtonStyle.primary, ButtonStyle.success,
            ButtonStyle.danger, ButtonStyle.gray]
    )
    await ctx.send("Choose major:", view=menu)

exported_commands = [change_role]
