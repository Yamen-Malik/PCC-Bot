from discord.ext.commands import Bot
import os

blacklist = ["bot_events.py"]
package = "events"

async def load_events(bot: Bot):
    """Loads all the bot events to the bot instance

    Args:
        bot (Bot): bot instance
    """

    # call setup and pass the bot instance to all .py files in the `package` folder
    for file in os.scandir(f"./{package}"):
        name, ext = os.path.splitext(file.name)
        if file.is_file() and ext == ".py" and file.name not in blacklist:
            module = f"{package}.{name}"
            await getattr(__import__(module), name).setup(bot)
