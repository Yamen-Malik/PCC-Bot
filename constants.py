from os import environ
TOKEN = environ["PCC_TOKEN"]
COMMAND_CHAR = ">"
MAX_POLL_OPTIONS = 10
MAX_POLL_OPTION_LENGTH = 40
DEFAULT_OPTION_EMOJIS = "🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯"
USER_MENTION = "$USER"
SERVER_MENTION = "$SERVER"
LOGS_FORMAT = "%(asctime)s | %(levelname)s | %(name)s: %(message)s"
LOGS_FILE = "logs.log"


DEFAULT_GUILD_DATA = {
    "welcome_messages": [
        f"Welcome {USER_MENTION} to {SERVER_MENTION}.",
    ],
    "welcome_new_members": True,
    "welcome_channel": "welcome",
    "new_member_roles": [],
    "polls": {}
}