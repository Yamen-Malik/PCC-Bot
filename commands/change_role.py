from discord.ext import commands
from discord import ButtonStyle
from utilities.choose_role import choose_role
from utilities.decorators import command
from utilities.menu import create_menu
from replit import db


@commands.command(name="change_role", help="Change your member role")
@command
async def change_role(ctx):
    styles = ButtonStyle
    menu = create_menu(
        db["new_member_roles"],
        choose_role,
        [styles.primary, styles.success, styles.danger, styles.gray]
    )
    await ctx.send("Choose major:", view=menu)