from discord import Interaction
from discord.ui import Button
from replit import db


async def choose_role(interaction: Interaction, button: Button) -> None:
    member = interaction.user
    guild = interaction.guild
    chosen_role_name = button.label

    if hasattr(member, "roles"):
        for role in member.roles:
            if role.name.lower() in map(lambda s: s.lower(), db[str(member.guild.id)]["new_member_roles"]):
                await member.remove_roles(role)
                break

    for role in guild.roles:
        if role.name.lower() == chosen_role_name.lower():
            await member.add_roles(role)
            await interaction.response.send_message(f"{member.mention} your role now is {chosen_role_name}", ephemeral=True)
            return
    await interaction.response.send_message("Failed to change role", ephemeral=True)
