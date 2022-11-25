from os import environ
TOKEN = environ['PCC_TOKEN']
COMMAND_CHAR = ">"
MAX_POLL_CHOICES = 10
MAX_POLL_CHOICE_LENGTH = 40
default_command_data = {"active": True, "channels": [],
                        "is_blacklist": True, "permissions": []}
