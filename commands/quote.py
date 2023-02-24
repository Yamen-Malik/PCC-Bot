from discord import app_commands, Interaction, Embed, Color
from discord.ext.commands import Cog, Bot
import requests


class Quote(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


    @app_commands.command(name="quote")
    async def quote(self, interaction: Interaction, id: str = "random") -> None:
        """Send a programming related quote by it's id, if id isn't provided return random quote

        Args:
            id (str, optional): id of the requested quote. Defaults to random
        """

        try:
            # send GET request to programming quotes api
            content = requests.get(
                f"https://programming-quotes-api.herokuapp.com/Quotes/{id}")
            if content.status_code == 404:
                await interaction.response.send_message("Invalid quote id", ephemeral=True)
                return False
            elif content.status_code != 200:
                raise Exception

            # load response and send it's content in an Embed object
            content = content.json()
            quote = Embed(
                title=content["author"], description=content["en"]+"\n\n"+content["id"], color=Color.gold())
            await interaction.response.send_message(embed=quote)
            return True
        except:
            await interaction.response.send_message("Error while requesting quote", ephemeral=True)
            return False


async def setup(bot: Bot) -> None:
    await bot.add_cog(Quote(bot))
