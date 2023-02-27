import asyncio
import logging
import sys

from discord import Intents
from discord.ext import commands
from discord.utils import setup_logging

from constants import COMMAND_CHAR, TOKEN, LOGS_FORMAT, LOGS_FILE
from error_handler import on_command_error
from package_loader import load_cogs
from keep_alive import keep_alive


# initialize the bot
intents = Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(
    intents=intents,
    command_prefix=COMMAND_CHAR,
    case_insensitive=True,
    help_command=None,
)
tree = bot.tree

# set default command handler
tree.on_error = on_command_error


# setup logger
setup_logging()
logger = logging.getLogger(f"Bot.{__name__.strip('_')}")

# setup a logging handler to print logs to a file
file_handler = logging.FileHandler(LOGS_FILE)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOGS_FORMAT)
file_handler.setFormatter(formatter)

# add handler to root logger
logging.getLogger().addHandler(file_handler)


# add all commands and events to current instance of the bot
logger.info("Loading Cogs and Groups")
asyncio.run(load_cogs(bot))


# run flask server to keep the bot running (needed for replit host)
keep_alive()
try:
    bot.run(TOKEN, log_handler=None)
except KeyboardInterrupt:
    bot.close()
except Exception as error:
    logger.error(error)
finally:
    logger.info("Bot terminated successfully")
    sys.exit(0)
