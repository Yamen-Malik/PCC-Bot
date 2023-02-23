from typing import Literal, Optional
from discord.ext import commands
from discord.ext.commands import Context


@commands.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: Context, spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    """Sync app commands with discord guild

    Args:
        spec (Optional[Literal[, optional): commands to sync. guild(~), all(*), clear(^). Defaults to all commands with all guilds
    """

    if spec == "~":
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
    elif spec == "*":
        ctx.bot.tree.copy_global_to(guild=ctx.guild)
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
    elif spec == "^":
        ctx.bot.tree.clear_commands(guild=ctx.guild)
        await ctx.bot.tree.sync(guild=ctx.guild)
        synced = []
    else:
        synced = await ctx.bot.tree.sync()
    await ctx.send(f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}")

exported_commands = [sync]
