from discord.ext import commands
from utils.decorators import command, edit_command


@commands.command(name="disable", help="Disable one of the bot commands")
@edit_command
@command
async def disable(ctx, command, command_data):
    command_data["active"] = False
    await ctx.send(f"{command} is disabled")


@commands.command(name="enable", help="Enable one of the bot commands")
@edit_command
@command
async def enable(ctx, command, command_data):
    command_data["active"] = True
    await ctx.send(f"{command} is enabled")

exported_commands = [disable, enable]
