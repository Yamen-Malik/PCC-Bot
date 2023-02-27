from logging import getLogger

from discord import Interaction
from discord.app_commands import (
    AppCommandError,
    MissingPermissions,
    BotMissingPermissions,
    CommandNotFound,
    CommandLimitReached,
    NoPrivateMessage,
    MissingRole,
    CommandOnCooldown,
)


async def on_command_error(interaction: Interaction, error: AppCommandError):
    """A callback that is called when any command raises an AppCommandError.

    Sends an error message to the user if the command does not have any error
    handlers attached to it.

    Args:
        interaction (Interaction): The interaction that is being handled.
        error (AppCommandError): The exception that was raised.
    """

    # ignore error if it's handled by local handler
    command = interaction.command
    if command and command._has_any_error_handlers():
        return

    # choose the appropriate message for the error
    message = ""
    if isinstance(error, MissingPermissions):
        message = "You don't have permission to run the the requested command!"
    elif isinstance(error, MissingRole):
        message = (
            "You don't have {error.missing_role} rule to run the the requested command!"
        )
    elif isinstance(error, MissingRole):
        message = "You don't have the required rule to run the the requested command!"
    elif isinstance(error, BotMissingPermissions):
        message = (
            "I don't have the permissions to do that!\n"
            "Please contact an admin to resolve the problem"
        )
    elif isinstance(error, CommandNotFound):
        message = "The requested command isn't found!"
    elif isinstance(error, CommandOnCooldown):
        message = "This command is on cooldown!\nPlease try again later."
    elif isinstance(error, CommandLimitReached):
        message = "Internal bot Error occurred!\nPlease try again later."
    elif isinstance(error, NoPrivateMessage):
        message = "The requested command is not available in private messages!"
    else:
        getLogger(__name__).warning(error)
        message = "Unknown Error occurred!"

    await interaction.response.send_message(message, ephemeral=True)
