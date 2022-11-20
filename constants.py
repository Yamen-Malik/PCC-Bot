from os import environ
TOKEN = environ['PCC_TOKEN']
COMMAND_CHAR = ">"
default_command_data = {"active": True, "channels": [],
                        "is_blacklist": True, "permissions": []}
