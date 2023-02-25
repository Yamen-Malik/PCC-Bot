from discord import app_commands, Interaction, Embed, Color
from discord.ext.commands import Cog, Bot
import requests


class Quote(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


    @app_commands.command(name="quote")
    @app_commands.checks.cooldown(150, 60)
    async def quote(self, interaction: Interaction, id: str = "random", tag: str = None) -> None:
        """Send a programming related quote by it's id, if id isn't provided return random quote

        Args:
            id (str): id of the requested quote. Defaults to random
            tag (str): tag of the random quote. Defaults to None
        """
        api_url = "https://api.quotable.io"
        try:
            # send GET request to programming quotes api
            if id == "random":
                endpoint = "/random"
                if tag:
                    endpoint += f"?tags={tag}" 
            else:
                endpoint = f"/quotes/{id}"

            content = requests.get(api_url + endpoint)
            if content.status_code == 404:
                if id == "random":
                    message = "Invalid quote tag!"
                else:
                    message = "Invalid quote id!"
                
                await interaction.response.send_message(message, ephemeral=True)
                return
            elif content.status_code != 200:
                raise Exception

            # load response and send it's content in an Embed object
            content = content.json()
            quote = Embed(
                title=content["author"], description=f"{content['content']}\n\nid: {content['_id']}", color=Color.gold())
            quote.add_field(name="",value="Powered by [quotable.io](https://quotable.io)", inline=False)
            await interaction.response.send_message(embed=quote)
        except:
            await interaction.response.send_message("Error while requesting quote!", ephemeral=True)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Quote(bot))
