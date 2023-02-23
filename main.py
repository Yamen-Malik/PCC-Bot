from discord import app_commands, Intents
from discord.ext import commands
from error_handler import on_command_error
from commands.all_commands import bot_commands
from events.all_events import bot_events
from constants import COMMAND_CHAR, TOKEN
from keep_alive import keep_alive

# initialize the bot
intents = Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(
    intents=intents, command_prefix=COMMAND_CHAR, case_insensitive=True)
tree = bot.tree

# set default command handler
tree.on_error = on_command_error


# add all the commands to current instance of the bot
for command in bot_commands:
    if isinstance(command, (app_commands.Command, app_commands.Group)):
        tree.add_command(command)
    elif isinstance(command, (commands.Command, commands.Group)):
        bot.add_command(command)

# add all the events to current instance of the bot
for event in bot_events:
    bot.add_listener(event)


# run flask server to keep the bot running (needed for replit host)
keep_alive()
try:
    bot.run(TOKEN)
except KeyboardInterrupt:
    bot.close()
finally:
    print('bot terminated successfully')
    exit(0)
