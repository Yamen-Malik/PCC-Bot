from discord.ext import commands
from replit import db
from major_menu import MajorMenu
import random


@commands.Cog.listener()
async def on_member_join(member):
    if not db["welcome_new_members"]:
        return
    for channel in member.guild.channels:
        if channel.name == db["welcome_channel"]:
            await channel.send(random.choice(db["welcome_messages"]).format(member.mention, member.guild.name))
            view = MajorMenu(member)
            await member.send(f"Select your major", view=view)
            break
