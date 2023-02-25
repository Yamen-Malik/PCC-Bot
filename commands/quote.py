from discord import app_commands, Interaction, Embed, Color
from discord.ext.commands import Cog, Bot
import requests
from logging import getLogger

class Quote(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = getLogger(__name__)


    @app_commands.command(name="quote")
    @app_commands.checks.cooldown(50, 60)
    async def quote(self, interaction: Interaction, tag: str = None) -> None:
        """Send a random quote

        Args:
            tag (str): tag of the random quote. Defaults to None
        """

        quote_api_url = "https://api.quotable.io"
        images_api_url = "https://images.quotable.dev/profile"
        try:
            # send GET request to quotes api
            endpoint = "/random"
            if tag:
                endpoint += f"?tags={tag}" 
            
            quote_response = requests.get(quote_api_url + endpoint)
            if quote_response.status_code == 404:
                await interaction.response.send_message("Invalid quote tag!", ephemeral=True)
                return
            elif quote_response.status_code != 200:
                raise Exception

            
            # load quote response content
            quote_content = quote_response.json()
            
            # send GET request to get the author's official or wikipedia page link
            author_link = None
            try:
                authors_response = requests.get(f"{quote_api_url}/authors?slug={quote_content['authorSlug']}")
                authors_content = authors_response.json()
                author_link = authors_content["results"][0]["link"]
            except Exception as e:
                self.logger.warning(f"Failed to retrieve author data due to the following exception:\n{e}")
                

            # create and send quote embed
            quote = Embed(description=quote_content['content'], color=Color.gold())
            
            # author image and link
            quote.set_thumbnail(url=f"{images_api_url}/200/{quote_content['authorSlug']}.jpg")
            quote.set_author(name=quote_content["author"], url=author_link)
            
            # credit 
            quote.add_field(name="",value="Powered by [quotable.io](https://quotable.io)", inline=False)

            await interaction.response.send_message(embed=quote)
        except Exception as e:
            self.logger.warning(e)
            await interaction.response.send_message("Error while requesting quote!", ephemeral=True)


async def setup(bot: Bot) -> None:
    await bot.add_cog(Quote(bot))
