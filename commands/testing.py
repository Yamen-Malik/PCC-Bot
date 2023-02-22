from discord import app_commands, Interaction, Permissions, User
from events.on_member_join import on_member_join


testing_group = app_commands.Group(name="testing", description="Group of commands used for testing", default_permissions=Permissions(manage_guild=True)) 

@testing_group.command(name="welcome")
@app_commands.checks.has_permissions(manage_guild=True)
async def welcome(interaction: Interaction, user: User=None) -> None:
    """Welcome a member to the server (used to test on_member_join)

    Args:
        user (User): user to mention in the welcome message. Defaults to the command caller
    """
    if not user:
        user = interaction.user
    await on_member_join(user)

exported_commands = [welcome]
