import os
from discord.ext.commands import Bot


blacklist = ["bot_commands.py"]
PACKAGE = "commands"


async def load_commands(bot: Bot):
    """Loads all the bot commands to the bot instance

    Args:
        bot (Bot): bot instance
    """

    # call setup and pass the bot instance to all .py files in the `package` folder
    for file in os.scandir(f"./{PACKAGE}"):
        name, ext = os.path.splitext(file.name)
        if file.is_file() and ext == ".py" and file.name not in blacklist:
            module = f"{PACKAGE}.{name}"
            await getattr(__import__(module), name).setup(bot)
