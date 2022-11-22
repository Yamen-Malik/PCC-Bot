from discord.ext import commands
from discord import ButtonStyle
from utilities.menu import create_menu
from utilities.choose_role import choose_role
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
            view = create_menu(db["new_member_roles"],
                               choose_role,
                               [styles.primary, styles.success,
                                   styles.danger, styles.gray]
                               )
            await channel.send(f"Select your major", view=view)
            break
