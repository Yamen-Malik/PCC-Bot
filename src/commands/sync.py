from typing import Literal, Optional
from logging import getLogger

from discord.ext import commands
from discord.ext.commands import Context, Cog, Bot


class Sync(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = getLogger(__name__)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        self,
        ctx: Context,
        mode: Optional[Literal["guild", "global"]] = "guild",
        only_guild_commands: bool = False,
    ) -> None:
        """Sync app commands with discord guild

        Args:
            mode (Optional[Literal[, optional): sync mode. guild(~), all(*). Defaults to guild
            only_guild_commands (bool): sync only guild commands, works only when mode is guild.
                Defaults to False
        """

        guild = ctx.guild
        if mode == "guild":
            if only_guild_commands:
                self.logger.info(
                    f"Syncing app commands with Guild({guild.name}, {guild.id})."
                )
            else:
                self.logger.info(
                    f"Syncing guild app commands with Guild({guild.name}, {guild.id})."
                )
                ctx.bot.tree.copy_global_to(guild=guild)

            synced = await ctx.bot.tree.sync(guild=guild)
        elif mode == "global":
            self.logger.info("Syncing app commands globally.")
            synced = await ctx.bot.tree.sync()
        else:
            await ctx.reply("Invalid mode!")
            return

        mode_message = "globally" if mode == "global" else "to the current guild"
        await ctx.reply(f"Synced {len(synced)} commands {mode_message}.")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def unsync(
        self, ctx: Context, mode: Optional[Literal["guild", "global"]] = "guild"
    ) -> None:
        """Un-Sync app commands with discord guild

        Args:
            mode (Optional[Literal[, optional): un-sync mode; guild or global. Defaults to guild
        """

        guild = ctx.guild
        if mode == "guild":
            self.logger.info(
                f"Un-Syncing guild app commands with Guild({guild.name}, {guild.id})."
            )
            self.bot.tree.clear_commands(guild=guild)
            await self.bot.tree.sync(guild=guild)
            await ctx.reply("Un-Synced guild.")
        elif mode == "global":
            self.logger.info("Un-Syncing app commands with all guilds.")
            self.bot.tree.clear_commands()
            await self.bot.tree.sync()
            await ctx.reply("Un-Synced global.")
        else:
            await ctx.reply("Invalid mode!")


async def setup(bot: Bot) -> None:
    await bot.add_cog(Sync(bot))
