from os import environ
TOKEN = environ['PCC_TOKEN']
COMMAND_CHAR = ">"
MAX_POLL_OPTIONS = 10
MAX_POLL_OPTION_LENGTH = 40
DEFAULT_OPTION_EMOJIS = "🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯"

DEFAULT_GUILD_DATA = {
    "welcome_messages": [
        "Welcome {} to {}.",
    ],
    "welcome_new_members": True,
    "welcome_channel": "welcome",
    "new_member_roles": [],
    "polls": {}
}