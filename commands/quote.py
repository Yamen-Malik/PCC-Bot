from logging import getLogger

import requests
from discord import app_commands, Interaction, Embed, Color
from discord.ext.commands import Bot


class Quote(app_commands.Group):
    """Interact with the quotes API"""

    quote_api_url = "https://api.quotable.io"
    images_api_url = "https://images.quotable.dev/profile"
    timeout = 5

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = getLogger(__name__)
        super().__init__()

    @app_commands.command()
    @app_commands.checks.cooldown(50, 60)
    async def random(self, interaction: Interaction, tag: str = None) -> None:
        """Send a random quote

        Args:
            tag (str): tag of the random quote. Defaults to None
        """

        # send GET request to quotes api
        endpoint = "/random"
        if tag:
            endpoint += f"?tags={tag}"

        quote_response = requests.get(
            self.quote_api_url + endpoint, timeout=self.timeout
        )
        if quote_response.status_code == 404:
            await interaction.response.send_message(
                "Invalid quote tag!", ephemeral=True
            )
            return
        if quote_response.status_code != 200:
            raise app_commands.AppCommandError(quote_response.json())

        # load quote response content
        quote_content = quote_response.json()

        # send GET request to get the author's official or wikipedia page link
        author_link = None
        try:
            authors_response = requests.get(
                f"{self.quote_api_url}/authors?slug={quote_content['authorSlug']}",
                timeout=self.timeout,
            )
            authors_content = authors_response.json()
            author_link = authors_content["results"][0]["link"]
        except Exception as error:
            self.logger.warning(
                f"Failed to retrieve author data due to the following exception:\n{error}"
            )

        # create and send quote embed
        quote = Embed(description=quote_content["content"], color=Color.gold())

        # author image and link
        quote.set_thumbnail(
            url=f"{self.images_api_url}/200/{quote_content['authorSlug']}.jpg"
        )
        quote.set_author(name=quote_content["author"], url=author_link)

        # credit
        quote.add_field(
            name="", value="Powered by [quotable.io](https://quotable.io)", inline=False
        )

        await interaction.response.send_message(embed=quote)

    @app_commands.command()
    @app_commands.checks.cooldown(2, 60)
    async def tags(self, interaction: Interaction) -> None:
        """Send a list of available quote tags sorted in descending order
        relative to the count of quotes
        """

        # send GET request to quotes api
        endpoint = "/tags"

        tags_response = requests.get(
            self.quote_api_url + endpoint, timeout=self.timeout
        )
        if tags_response.status_code != 200:
            raise app_commands.AppCommandError(tags_response.json())

        # load tags response content
        tags_content = tags_response.json()

        # sort tags in descending order
        tags_content = sorted(tags_content, key=lambda x: x["quoteCount"], reverse=True)

        # load and format tag names
        tags = list(map(lambda x: x["name"], tags_content))
        tags = ", ".join(tags)

        # create and send quote embed
        quote = Embed(title="Tags", description=tags, color=Color.brand_green())

        # credit
        quote.add_field(
            name="", value="Powered by [quotable.io](https://quotable.io)", inline=False
        )

        await interaction.response.send_message(embed=quote)

    async def on_error(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ) -> None:
        """A callback that is called when a child's command raises an AppCommandError

        Args:
            interaction (Interaction): The interaction that is being handled.
            error (app_commands.AppCommandError): the exception that was raised.
        """

        self.logger.warning(error)
        await interaction.response.send_message(
            "Error while requesting data from the quote API!", ephemeral=True
        )


async def setup(bot: Bot) -> None:
    bot.tree.add_command(Quote(bot))
