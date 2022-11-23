from discord.ext import commands
from discord import ButtonStyle
from utils.menu.menu import create_menu
from utils.major.major import choose_major
from replit import db
import random


@commands.Cog.listener()
async def on_member_join(member):
    if not db["welcome_new_members"]:
        return
    for channel in member.guild.channels:
        if channel.name == db["welcome_channel"]:
            await channel.send(random.choice(db["welcome_messages"]).format(member.mention, member.guild.name))
            styles = ButtonStyle
            view = create_menu(
                ['Computer Science', 'Software Engineering',
                    'Cyber Security', 'Artificial Intelligence'],
                [choose_major]*3,
                [styles.primary, styles.success, styles.danger]
            )
            await member.send(f"Select your major", view=view)
            break
