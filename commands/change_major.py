from discord.ext import commands
from discord import ButtonStyle
from events.on_member_join import choose_major
from commands.decorators import command
from menu import create_menu
from replit import db

@commands.command(name="change_major", help="Change your major role")
@command
async def change_major(ctx):
    styles = ButtonStyle
    menu = create_menu(
        db["new_member_roles"],
        [choose_major]*4,
        [styles.primary, styles.success, styles.danger, styles.gray]
    )
    await ctx.send("Choose major:", view=menu)
