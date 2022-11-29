### Event code template
```python
from discord.ext import commands

@commands.Cog.listener()
async def event_name():

    pass

exported_events = [event_name]
```