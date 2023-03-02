from discord import ButtonStyle, app_commands, Interaction
from discord.ext.commands import Cog, Bot
from replit import db

from utils.choose_role import choose_role
from utils.menu import create_menu


class ChangeRole(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command(name="change_role")
    @app_commands.guild_only()
    async def change_role(self, interaction: Interaction) -> None:
        """Change your member role to any of the public roles"""

        roles = db[str(interaction.guild.id)]["new_member_roles"]
        if len(roles) < 2:
            await interaction.response.send_message(
                "No available roles to choose from!", ephemeral=True
            )

        menu = create_menu(
            roles,
            [choose_role],
            [
                ButtonStyle.primary,
                ButtonStyle.success,
                ButtonStyle.danger,
                ButtonStyle.gray,
            ],
        )
        await interaction.response.send_message(
            "Choose role:", view=menu, ephemeral=True
        )


async def setup(bot: Bot) -> None:
    await bot.add_cog(ChangeRole(bot))
