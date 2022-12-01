from replit import db
from constants import DEFAULT_COMMAND_DATA
from discord.errors import NotFound

command_names = []


def get_command_data(guild_id, command: str) -> dict:
    commands = db[str(guild_id)].get("commands", {})
    commands[command] = commands.get(command, DEFAULT_COMMAND_DATA)
    db[str(guild_id)]["commands"] = commands
    return commands[command]


def command(func):
    command_names.append(func.__name__)

    async def wrapper(ctx, *args, **kwargs):
        data = get_command_data(ctx.guild.id, func.__name__)
        if data["active"] and data["is_blacklist"] != (ctx.channel.name.lower() in data["channels"]):
            if all([getattr(ctx.permissions, perm) for perm in data["permissions"]]):
                should_delete_message = db[str(ctx.guild.id)]["delete_command_call_message"]
                if await func(ctx, *args, **kwargs) and should_delete_message:
                    try:
                        await ctx.message.delete()
                    except NotFound:
                        pass                    
            else:
                await ctx.send(f"Missing Permissions to run {func.__name__}")
    return wrapper


def edit_command(func):
    async def wrapper(ctx, command, *args, **kwargs):
        command = command.lower()
        if command in command_names:
            data = get_command_data(ctx.guild.id, command)
            return await func(ctx, command, data, *args, **kwargs)
        else:
            print(f"{command} is not a command")

    return wrapper
