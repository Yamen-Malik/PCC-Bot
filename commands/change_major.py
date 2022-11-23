from discord.ext import commands
from discord import ButtonStyle
from utils.major.major import choose_major
from utils.menu.menu import create_menu
from commands.decorators import command


@commands.command(name="change_major", help="Change your major role")
@command
async def change_major(ctx):
    styles = ButtonStyle
    menu = create_menu(
        ['Computer Science', 'Software Engineering',
            'Cyber Security', 'Artificial Intelligence'],
        [choose_major]*3,
        [styles.primary, styles.success, styles.danger]
    )
    await ctx.send("Choose major:", view=menu)
