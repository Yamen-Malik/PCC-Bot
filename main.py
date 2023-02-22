from events.all_events import bot_events
from commands.all_commands import bot_commands
import discord
from discord.ext import commands
from keep_alive import keep_alive
from constants import COMMAND_CHAR, TOKEN
from error_handler import on_command_error

# initialize the bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(
    intents=intents, command_prefix=COMMAND_CHAR, case_insensitive=True)
tree = bot.tree

# set default command handler
tree.on_error = on_command_error


@bot.event
async def on_ready():
    await tree.sync()
    print("Synced with all guilds")
    print("Running")


# add all the commands to current instance of the bot
for command in bot_commands:
    tree.add_command(command)

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
