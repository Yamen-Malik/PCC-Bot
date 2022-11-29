from discord.ext import commands
from utils.decorators import command


@commands.command(name="delete", help="Delete last n messages")
@command
async def delete(ctx: commands.Context, x: int,) -> bool:
    try:
        member_id = n = None
        if x.startswith("<"):
            member_id = int(x[2:-1])
        else:
            n = int(x)

        if member_id:
            await ctx.channel.purge(check=lambda m: m.author.id == member_id)
        else:
            await ctx.channel.purge(limit=n+1)
        return True
    except:
        print("Invalid delete argument")
        return False

exported_commands = [delete]
