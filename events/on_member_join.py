from discord.ext import commands
from discord import ButtonStyle, Interaction, Button
from menu import create_menu
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
                [choose_major]*3,
                [styles.primary, styles.success, styles.danger, styles.gray]
            )
            await member.send(f"Select your major", view=view)
            break


async def choose_major(interaction: Interaction, button: Button):
    member = interaction.user
    major = button.label
    role = None
    for r in member.guild.roles:
        if r.name.lower() == major.lower():
            role = r
    if role:
        await member.add_roles(role)
        await interaction.channel.send(f"{member.mention} your role now is {major}")
        await interaction.message.delete()
    else:
        await interaction.channel.send(f'failed to change role')
