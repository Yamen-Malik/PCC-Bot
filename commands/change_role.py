from discord import ButtonStyle, app_commands, Interaction
from utils.choose_role import choose_role
from utils.menu import create_menu
from replit import db


@app_commands.command(name="change_role")
async def change_role(interaction: Interaction) -> None:
    """Change your member role to your academic major
    """
    
    roles = db[str(interaction.guild.id)]["new_member_roles"]
    if len(roles) < 1:
        await interaction.response.send_message("No majors to choose from.", ephemeral=True)

    menu = create_menu(
        roles,
        [choose_role],
        [ButtonStyle.primary, ButtonStyle.success,
            ButtonStyle.danger, ButtonStyle.gray]
    )
    await interaction.response.send_message("Choose major:", view=menu, ephemeral=True)

exported_commands = [change_role]
