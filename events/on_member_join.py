from discord.ext import commands
from discord import ButtonStyle
from utils.menu import create_menu
from utils.choose_role import choose_role
from replit import db
import random


@commands.Cog.listener()
async def on_member_join(member):
    guild_db = db[member.guild.id]
    if not guild_db["welcome_new_members"]:
        return
    for channel in member.guild.channels:
        if channel.name == guild_db["welcome_channel"]:
            await channel.send(random.choice(guild_db["welcome_messages"]).format(member.mention, member.guild.name))
            styles = ButtonStyle
            view = create_menu(
                guild_db["new_member_roles"],
                [choose_role],
                [styles.primary, styles.success,
                 styles.danger, styles.gray]
            )
            await channel.send(f"Select your major", view=view)
            break

exported_events = [on_member_join]
