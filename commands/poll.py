from typing import Literal

from discord import (
    app_commands,
    Embed,
    PartialEmoji,
    Color,
    Interaction,
    Button,
    AllowedMentions,
)
from discord.ext.commands import Bot
from emoji import is_emoji
from replit import db

from constants import MAX_POLL_OPTIONS, MAX_POLL_OPTION_LENGTH, DEFAULT_OPTION_EMOJIS
from utils.menu import create_menu


@app_commands.guild_only()
class Poll(app_commands.Group):
    """Create a poll for members to vote on"""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()

    async def validate_options(
        self, interaction: Interaction, options: list[str]
    ) -> bool:
        """Validates the given options and sends an error message to the channel
        if options are not valid

        Args:
            options (list[str]): list of options to validate

        Returns:
            bool:True if options are valid, False otherwise
        """

        for i in range(len(options) - 1, -1, -1):
            j = options.index(options[i])
            if j != i:
                options.pop(j)

        if len(options) > MAX_POLL_OPTIONS:
            await interaction.response.send_message(
                f"Poll must have at most {MAX_POLL_OPTIONS} options!", ephemeral=True
            )
            return False
        if len(options) < 2:
            await interaction.response.send_message(
                "Poll must have at least unique 2 options!", ephemeral=True
            )
            return False
        if isinstance(options[0], str) and not all(
            len(option) <= MAX_POLL_OPTION_LENGTH for option in options
        ):
            await interaction.response.send_message(
                f"Option name length must be at most {MAX_POLL_OPTIONS} characters!",
                ephemeral=True,
            )

            return False

        return True

    async def get_poll(self, interaction: Interaction, poll_name: str) -> dict:
        """Returns the poll data from the database if it exists, otherwise sends an error
        message to the channel and returns None

        Args:
            poll_name (str): name fo the requested poll

        Returns:
            dict: poll data
        """

        poll = db[str(interaction.guild.id)]["polls"].get(poll_name.lower())
        if not poll:
            await interaction.response.send_message(
                f"{poll_name} poll is not found.", ephemeral=True
            )
        return poll

    async def handle_anonymous_votes(
        self, interaction: Interaction, button: Button
    ) -> None:
        """Handles the scores when a vote button is clicked

        Args:
            button (Button): clicked button
        """

        # get poll data
        poll_name = interaction.message.embeds[0].title
        poll = await self.get_poll(interaction, poll_name)

        # check if poll data is available and allow members to vote only once
        member_id = interaction.user.id
        if not poll:
            await interaction.response.send_message(
                "The poll you trying to vote on is no longer available!", ephemeral=True
            )
            return
        if member_id in poll["voters"]:
            await interaction.response.send_message(
                "You've already voted on this poll!", ephemeral=True
            )
            return

        option = button.label
        poll["voters"].append(member_id)
        poll["votes"][option] += 1
        await interaction.response.defer()

    @app_commands.command(name="reactions")
    async def poll_reactions(
        self,
        interaction: Interaction,
        poll_name: str,
        options: str,
        emojis: str = DEFAULT_OPTION_EMOJIS,
        mention: Literal["everyone", "here"] = "",
    ) -> None:
        """Create a poll where message reactions are used to vote

        Args:
            poll_name (str): name of the new poll
            options (str): list of options separated by a comma (,)
            emojis (str): list of emojis to use for voting separated by white space.
                Defaults to a list of alphabet emojis
            mention (str): Mention type. Defaults to None
        """

        options = [s.strip() for s in options.split(",")]

        # cut down default emojis to the number of options
        if emojis == DEFAULT_OPTION_EMOJIS:
            emojis = emojis[: len(options) * 2]

        # only allow unicode or guild emojis
        emojis = emojis.split()
        for i, emoji in enumerate(emojis):
            partial_emoji = PartialEmoji.from_str(emoji)
            if not is_emoji(emoji) and partial_emoji not in interaction.guild.emojis:
                await interaction.response.send_message(
                    "Invalid emoji! Please only use emojis that are available on this server.",
                    ephemeral=True,
                )
                return

            emojis[i] = partial_emoji

        # validate options and emojis
        if len(options) != len(emojis):
            await interaction.response.send_message(
                "Every option should have an emoji!", ephemeral=True
            )
            return
        if not all(
            emoji.is_unicode_emoji() or emoji.is_custom_emoji() for emoji in emojis
        ):
            await interaction.response.send_message("Invalid emoji!", ephemeral=True)
            return
        if not (
            await self.validate_options(interaction, options)
            and await self.validate_options(interaction, emojis)
        ):
            return
        # this check should stay after the validate_options call
        # since validate_options removes duplicates
        if len(options) != len(emojis):
            await interaction.response.send_message(
                "Duplicate emojis/options are not allowed in polls", ephemeral=True
            )
            return

        # create poll embed
        desc = "\n".join(f"{option} {emoji}" for option, emoji in zip(options, emojis))
        embed = Embed(title=poll_name, description=desc, color=Color.blue())
        embed.set_author(
            name=interaction.user.display_name, icon_url=interaction.user.avatar
        )

        # add mention only if user has permission to mention everyone
        if mention:
            if not interaction.user.guild_permissions.mention_everyone:
                await interaction.response.send_message(
                    (
                        "You don't have permission to mention members!\n"
                        "Please try again without mention."
                    ),
                    ephemeral=True,
                )
                return
            mention = f"@{mention}"

        # send message
        allowed_mentions = AllowedMentions(everyone=True)
        await interaction.response.send_message(
            content=mention, allowed_mentions=allowed_mentions, embed=embed
        )

        # react to the sent poll message with all given emojis to make voting easier for members
        message = await interaction.original_response()
        for emoji in emojis:
            await message.add_reaction(str(emoji))

    @app_commands.command(name="anonymous")
    async def poll_anonymous(
        self,
        interaction: Interaction,
        poll_name: str,
        options: str,
        public_results: bool = True,
        mention: Literal["everyone", "here"] = "",
    ) -> None:
        """Create an anonymous poll using view and buttons

        Args:
            poll_name (str): name of the new poll
            options (str): list of options separated by a comma (,)
            public_results (bool): Allow members to view results while the poll is still open.
                Defaults to True
            mention (str): Mention type. Defaults to None
        """

        guild_db = db[str(interaction.guild.id)]

        if poll_name.lower() in map(lambda s: s, guild_db["polls"].keys()):
            await interaction.response.send_message(
                "Poll already exists.", ephemeral=True
            )
            return

        options = [s.strip() for s in options.split(",")]
        if not await self.validate_options(interaction, options):
            return

        # create poll view and embed
        view = create_menu(options, [self.handle_anonymous_votes])

        embed = Embed(title=poll_name, color=Color.blue())
        embed.set_author(
            name=interaction.user.display_name, icon_url=interaction.user.avatar
        )
        embed.add_field(name="status", value="*Open*", inline=False)

        # add mention only if user has permission to mention everyone
        if mention:
            if not interaction.user.guild_permissions.mention_everyone:
                await interaction.response.send_message(
                    (
                        "You don't have permission to mention members!\n"
                        "Please try again without mention."
                    ),
                    ephemeral=True,
                )
                return
            mention = f"@{mention}"

        # send message
        allowed_mentions = AllowedMentions(everyone=True)
        await interaction.response.send_message(
            content=mention, allowed_mentions=allowed_mentions, embed=embed, view=view
        )

        # add poll data to the database
        message = await interaction.original_response()
        guild_db["polls"][poll_name.lower()] = {
            "voters": [],
            "votes": {option: 0 for option in options},
            "channel_id": interaction.channel.id,
            "message_id": message.id,
            "author_id": interaction.user.id,
            "public_results": public_results,
        }

    @app_commands.command(name="list")
    @app_commands.checks.has_permissions(administrator=True)
    async def list(self, interaction: Interaction) -> None:
        """List all open polls (works only for anonymous polls)"""

        # load and format polls data in an embed
        polls = db[str(interaction.guild.id)]["polls"]
        embed = Embed(title="Open polls", color=Color.yellow())
        bot = interaction.client
        i = 1
        # add an embed field for each poll and include the author and channel in that field
        for name, data in polls.items():
            user = bot.get_user(data["author_id"]).name
            channel = bot.get_channel(data["channel_id"]).name
            embed.add_field(
                name=f"{i}. {name.capitalize()}",
                value=f"Author: {user}\nChannel: {channel}",
                inline=False,
            )
            i += 1

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="result")
    async def result(self, interaction: Interaction, poll_name: str) -> None:
        """Send the result of the requested poll (works only for anonymous poll)

        Args:
            poll_name (str): name of the requested poll
        """

        poll = await self.get_poll(interaction, poll_name)
        if not poll:
            return

        # Only send the results if they are public or if the request is from the author or an admin
        if (
            not poll["public_results"]
            and poll["author_id"] != interaction.user.id
            and not interaction.user.guild_permissions.manage_messages
        ):
            await interaction.response.send_message(
                "You don't have permission to view the results of this poll.",
                ephemeral=True,
            )
            return

        # load and format votes
        votes = poll["votes"]
        sorted_keys = sorted(votes, key=lambda k: votes[k], reverse=True)
        result_str = "\n".join([f"{k}: {votes[k]}" for k in sorted_keys])

        # create and send results message
        embed = Embed(
            title=f"{poll_name} results", description=result_str, color=Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="close")
    async def close(self, interaction: Interaction, poll_name: str) -> None:
        """Close the requested poll (works only for anonymous poll)

        Args:
            poll_name (str): name of the requested poll
        """

        poll = await self.get_poll(interaction, poll_name)
        if not poll:
            return

        # Only allow author and admins to close the poll
        if (
            poll["author_id"] != interaction.user.id
            and not interaction.user.guild_permissions.manage_messages
        ):
            await interaction.response.send_message(
                "You don't have permission to close polls that you don't own.",
                ephemeral=True,
            )
            return

        channel = await interaction.guild.fetch_channel(poll["channel_id"])
        message = await channel.fetch_message(poll["message_id"])

        # change the status of the poll message to Closed and change the embed color to red
        embed = message.embeds[0]
        embed.color = Color.dark_red()
        embed.set_field_at(
            index=len(message.embeds) - 1, name="status", value="*Closed*", inline=False
        )
        await message.edit(view=None, embed=embed)

        # send poll result
        await self.get_command("result").callback(self, interaction, poll_name)

        # delete poll data and confirm that the poll has been closed
        del db[str(interaction.guild.id)]["polls"][poll_name.lower()]
        await interaction.followup.send(f"{poll_name} poll has been closed.")


async def setup(bot: Bot) -> None:
    bot.tree.add_command(Poll(bot))
