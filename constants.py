from os import environ
TOKEN = environ['PCC_TOKEN']
COMMAND_CHAR = ">"
MAX_POLL_CHOICES = 10
MAX_POLL_CHOICE_LENGTH = 40
DEFAULT_COMMAND_DATA = {"active": True, "channels": [],
                        "is_blacklist": True, "permissions": []}

MANAGE_GUILD = DEFAULT_COMMAND_DATA.copy()
MANAGE_GUILD["permissions"].append("manage_guild")

MANAGE_MESSAGES = DEFAULT_COMMAND_DATA.copy()
MANAGE_MESSAGES["permissions"].append("manage_messages")

DEFAULT_GUILD_DATA = {
    "welcome_messages": [
        "Welcome {} to {}.",
    ],
    "welcome_new_members": True,
    "new_member_roles": [],
    "delete_command_call_message": True,
    "commands": {
        "poll_anonymous": MANAGE_GUILD,
        "result":   MANAGE_GUILD,
        "close":    MANAGE_GUILD,
        "disable":  MANAGE_GUILD,
        "enable":   MANAGE_GUILD,
        "delete":   MANAGE_MESSAGES,
    },
    "polls": {},
}
