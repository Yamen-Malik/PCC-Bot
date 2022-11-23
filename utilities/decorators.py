from replit import db
from constants import default_command_data

command_names = []


def get_command_data(command: str) -> dict:
    commands = db.get("commands", {})
    commands[command] = commands.get(command, default_command_data)
    db["commands"] = commands
    return commands[command]


def command(func):
    command_names.append(func.__name__)

    async def wrapper(ctx, *args, **kwargs):
        data = get_command_data(func.__name__)
        if data["active"] and data["is_blacklist"] != (ctx.channel.name.lower() in data["channels"]):
            if all([getattr(ctx.permissions, perm) for perm in data["permissions"]]):
                return await func(ctx, *args, **kwargs)
            else:
                await ctx.send(f"Missing Permissions to run {func.__name__}")
    return wrapper


def edit_command(func):
    async def wrapper(ctx, command, *args, **kwargs):
        command = command.lower()
        if command in command_names:
            data = get_command_data(command)
            return await func(ctx, command, data, *args, **kwargs)
        else:
            print(f"{command} is not a command")

    return wrapper