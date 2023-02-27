## Event file template
```python
from discord.ext.commands import Cog, Bot


class CogName(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def event_name(self):

        pass


async def setup(bot: Bot) -> None:
    await bot.add_cog(CogName(bot))
```