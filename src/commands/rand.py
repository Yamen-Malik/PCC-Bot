import random

from discord import app_commands, Interaction
from discord.ext.commands import Bot


class Random(app_commands.Group):
    """Send a random number, choice or user"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    async def send_random_number(
        self, interaction: Interaction, lower, upper, is_int: bool
    ) -> None:
        """
        Generates and sends a random number in the given range

        Sends an error message if the range isn't valid
        """
        try:
            lower = float(lower)
            upper = float(upper)
            if lower > upper:
                lower, upper = upper, lower

            result = (
                random.randint(lower, upper) if is_int else random.uniform(upper, lower)
            )
        except ValueError:
            await interaction.response.send_message(
                "Invalid lower or upper value", ephemeral=True
            )

        await interaction.response.send_message(result)

    @app_commands.command(name="number")
    async def random_number(
        self, interaction: Interaction, lower: float = 0.0, upper: float = 1.0
    ) -> None:
        """Send a random number in the given range [l, u)

        Args:
            lower (float): lower limit of the range (included). Defaults to 0
            upper (float): upper limit of the range (excluded). Defaults to 1
        """

        await self.send_random_number(interaction, lower, upper, False)

    @app_commands.command(name="integer")
    async def random_int(
        self, interaction: Interaction, lower: int = 0, upper: int = 100
    ) -> None:
        """Send a random integer in the given range [l, u]

        Args:
            interaction (Interaction): _description_
            lower (int, optional): lower limit of the range (included). Defaults to 0.
            upper (int, optional): upper limit of the range (included). Defaults to 100.
        """

        await self.send_random_number(interaction, lower, upper, True)

    @app_commands.command(name="choice")
    async def random_choice(self, interaction: Interaction, values: str) -> None:
        """Returns a random value from the given values

        Args:
            values (str): list of values to pick from separated by a comma (,)
        """

        try:
            assert values
            values_list = [s.strip() for s in values.strip().split(",")]
            assert len(values_list) > 1
            await interaction.response.send_message(random.choice(values_list))
        except AssertionError:
            await interaction.response.send_message("Invalid input", ephemeral=True)

    @app_commands.command(name="user")
    @app_commands.checks.has_permissions(mention_everyone=True)
    async def random_user(
        self, interaction: Interaction, server_wide: bool = False
    ) -> None:
        """Mention a random member from the channel or from the whole server if server_wide is true

        Args:
            server_wide (bool, optional): include users that are not in the current channel.
                Defaults to False
        """

        if server_wide:
            members = interaction.guild.members
        else:
            members = interaction.channel.members
        await interaction.response.send_message(random.choice(members).mention)


async def setup(bot: Bot) -> None:
    bot.tree.add_command(Random(bot))
