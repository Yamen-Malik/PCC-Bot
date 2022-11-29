from discord.ext import commands
from utils.decorators import command, edit_command


@commands.command(name="disable", help="Disable one of the bot commands")
@edit_command
@command
async def disable(ctx: commands.Context, command: str, command_data: dict) -> bool:
    command_data["active"] = False
    await ctx.send(f"{command} is disabled")
    return True


@commands.command(name="enable", help="Enable one of the bot commands")
@edit_command
@command
async def enable(ctx: commands.Context, command: str, command_data: dict) -> bool:
    command_data["active"] = True
    await ctx.send(f"{command} is enabled")
    return True

exported_commands = [disable, enable]
