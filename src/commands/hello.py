from discord import app_commands, Interaction
from discord.ext.commands import Cog, Bot


class Hello(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command(name="hello")
    async def hello(self, interaction: Interaction) -> None:
        """Say hello to the bot"""

        await interaction.response.send_message(
            f"Hi {interaction.user.mention}.", ephemeral=True
        )


async def setup(bot: Bot) -> None:
    await bot.add_cog(Hello(bot))
