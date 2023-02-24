from discord import app_commands, Interaction, User
from discord.ext.commands import Bot
from logging import getLogger


@app_commands.default_permissions(manage_guild=True)
class Testing(app_commands.Group):
    """Group of commands used for testing
    """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = getLogger(__name__)
        super().__init__()


    @app_commands.command(name="welcome")
    async def welcome(self, interaction: Interaction, user: User=None) -> None:
        """Welcome a member to the server (used to test on_member_join)

        Args:
            user (User): user to mention in the welcome message. Defaults to the command caller
        """
        
        if not user:
            user = interaction.user
        self.logger.debug("Dispatching on_member_join event manually")
        self.bot.dispatch("member_join", user)

        await interaction.response.send_message("Welcome message is sent.", ephemeral=True)


async def setup(bot: Bot) -> None:
    bot.tree.add_command(Testing(bot))