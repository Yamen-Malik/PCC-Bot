from logging import getLogger

from discord import app_commands, Interaction
from discord.ext.commands import Cog, Bot


class Delete(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = getLogger(__name__)

    @app_commands.command(name="delete")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_messages=True)
    async def delete(
        self,
        interaction: Interaction,
        count: int,
    ) -> None:
        """Delete last n messages in this channel

        Args:
            count (int): number of messages to delete
        """

        try:
            assert isinstance(count, int)
            await interaction.response.send_message(
                f"Deleting {count} message{'s'*(count>1)}", ephemeral=True
            )
            await interaction.channel.purge(limit=count)
        except AssertionError:
            await interaction.response.send_message(
                "Invalid delete argument.", ephemeral=True
            )
        except Exception as error:
            self.logger.warning(error)
            await interaction.response.send_message(
                "Error occurred while deleting the messages", ephemeral=True
            )


async def setup(bot: Bot) -> None:
    await bot.add_cog(Delete(bot))
