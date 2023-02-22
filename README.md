### Command code template
```python
from discord import app_commands, Interaction

@app_commands.command(name="command_name")
async def command_name(interaction: Interaction) -> None:
    """Command description

    Args:
        parameter (type): description. Defaults to value
    """    

    pass

exported_commands = [command_name]
```