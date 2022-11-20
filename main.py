from events import all_events
from commands import all_commands
import discord
from discord.ext import commands
from keep_alive import keep_alive
from constants import COMMAND_CHAR, TOKEN


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(
    intents=intents, command_prefix=COMMAND_CHAR, case_insensitive=True)


# add all the commands to current instance of the bot
for name in all_commands.__dict__:
    attr = getattr(all_commands, name)
    if isinstance(attr, commands.Command):
        bot.add_command(attr)

# add all the events to current instance of the bot
for name in all_events.__dict__:
    attr = getattr(all_events, name)
    if isinstance(attr, commands.Cog):
        bot.add_cog(attr)

# run flask server to keep the bot running (needed for replit host)
keep_alive()
bot.run(TOKEN)
