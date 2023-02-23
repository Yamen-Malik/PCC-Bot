from discord import app_commands, Intents
from discord.ext import commands
from discord.utils import setup_logging
from constants import COMMAND_CHAR, TOKEN, LOGS_FORMAT, LOGS_FILE
from error_handler import on_command_error
from commands.all_commands import bot_commands
from events.all_events import bot_events
from keep_alive import keep_alive
import logging


# initialize the bot
intents = Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(
    intents=intents, command_prefix=COMMAND_CHAR, case_insensitive=True)
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


# add all the commands to current instance of the bot
logger.info("Adding commands")
for command in bot_commands:
    if isinstance(command, (app_commands.Command, app_commands.Group)):
        tree.add_command(command)
    elif isinstance(command, (commands.Command, commands.Group)):
        bot.add_command(command)
    else:
        logger.error(f"Invalid command type: {type(command)}")

# add all the events to current instance of the bot
logger.info("Adding events")
for event in bot_events:
    bot.add_listener(event)


# run flask server to keep the bot running (needed for replit host)
keep_alive()
try:
    bot.run(TOKEN, log_handler=None)
except KeyboardInterrupt:
    bot.close()
finally:
    logger.info("Bot terminated successfully")
    exit(0)
