from discord.ext import commands
from discord import ButtonStyle, Member
from utils.menu import create_menu
from utils.choose_role import choose_role
from replit import db
from constants import USER_MENTION, SERVER_MENTION
import random


@commands.Cog.listener()
async def on_member_join(member: Member):
    guild_db = db[str(member.guild.id)]
    if not guild_db["welcome_new_members"]:
        return

    channel = None
    for ch in member.guild.channels:
        if ch.name.lower() == guild_db["welcome_channel"].lower():
            channel = ch
            break
    
    if not channel:
        print("welcome channel is not found")
        return

    message = random.choice(guild_db["welcome_messages"])
    message = message.replace(USER_MENTION, member.mention)
    message = message.replace(SERVER_MENTION, member.guild.name)
    await channel.send(message)

    if len(guild_db["new_member_roles"]) > 1:
        view = create_menu(
            guild_db["new_member_roles"],
            [choose_role],
            [ButtonStyle.primary, ButtonStyle.success,
             ButtonStyle.danger, ButtonStyle.gray]
        )
        await channel.send(f"Select your major", view=view)
    elif len(guild_db["new_member_roles"]) == 1:
        role_name = guild_db["new_member_roles"][0].lower()
        for role in member.guild.roles:
            if role.name.lower() == role_name:
                await member.add_roles(role)
                break

exported_events = [on_member_join]
