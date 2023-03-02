from discord import Interaction
from discord.ui import Button
from discord.errors import NotFound
from replit import db


async def choose_role(
    interaction: Interaction, button: Button, owner_id: int = None
) -> None:
    member = interaction.user
    guild = interaction.guild
    chosen_role_name = button.label

    # check if the interaction user is the owner
    if owner_id is not None and member.id != owner_id:
        await interaction.response.send_message(
            "This dialog is exclusive to another member!", ephemeral=True
        )
        return

    # remove existing 'new member role' from the the member
    if hasattr(member, "roles"):
        guild_roles = list(
            map(lambda s: s.lower(), db[str(member.guild.id)]["new_member_roles"])
        )
        for role in member.roles:
            if role.name.lower() in guild_roles:
                await member.remove_roles(role)
                break

    # get chosen role
    chosen_role = None
    for role in guild.roles:
        if role.name.lower() == chosen_role_name.lower():
            chosen_role = role
            break

    # return if role is not found
    if chosen_role is None:
        await interaction.response.send_message(
            "Role doesn't exist! Please inform server admins.", ephemeral=True
        )
        return

    # add role
    await member.add_roles(chosen_role)
    await interaction.response.send_message(
        f"{member.mention} your role now is {chosen_role_name}", ephemeral=True
    )

    # delete the message after as member has chooses their role
    try:
        await interaction.message.delete()
    except NotFound:
        # this will trigger if the message was ephemeral
        pass
