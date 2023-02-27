## Command file template

### Using Cogs
```python
from discord import app_commands, Interaction
from discord.ext.commands import Cog, Bot


class CogName(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command(name="command display name")
    async def command_name(self, interaction: Interaction) -> None:
        """Command description

        Args:
            parameter (type): description. Defaults to value
        """

        pass


async def setup(bot: Bot) -> None:
    await bot.add_cog(CogName(bot))
```

### Using Groups
```python
from discord import app_commands, Interaction
from discord.ext.commands import Bot


class GroupName(app_commands.Group):
    """Group description
    """
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="command display name")
    async def command_name(self, interaction: Interaction) -> None:
        """Command description

        Args:
            parameter (type): description. Defaults to value
        """

        pass


async def setup(bot: Bot) -> None:
    await bot.tree.add_command(GroupName(bot))
```