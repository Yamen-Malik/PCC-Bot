from discord import app_commands, Embed, PartialEmoji, Color, Interaction, Button
from constants import MAX_POLL_OPTIONS, MAX_POLL_OPTION_LENGTH, DEFAULT_OPTION_EMOJIS
from utils.menu import create_menu
from replit import db


poll_group = app_commands.Group(name="poll", description="Create a poll for members to vote on")

async def validate_options(interaction: Interaction, options: list[str]) -> bool:
    """Validates the given options and sends an error message to the channel if options are not valid

    Args:
        options (list[str]): list of options to validate

    Returns:
        bool:True if options are valid, False otherwise
    """

    for i in range(len(options)-1, -1, -1):
        j = options.index(options[i])
        if j != i:
            options.pop(j)

    if len(options) > MAX_POLL_OPTIONS:
        await interaction.response.send_message(f"Poll must have at most {MAX_POLL_OPTIONS} options!", ephemeral=True)
        return False
    elif len(options) < 2:
        await interaction.response.send_message("Poll must have at least 2 options!", ephemeral=True)
        return False
    elif type(options[0]) == str and not all(len(option) <= MAX_POLL_OPTION_LENGTH for option in options):
        await interaction.response.send_message(f"Option name length must be at most {MAX_POLL_OPTIONS} characters!", ephemeral=True)
        return False

    return True

async def get_poll(interaction: Interaction, poll_name: str) -> dict:
    """Returns the poll data from the database if it exists, otherwise sends an error message to the channel and returns None

    Args:
        poll_name (str): name fo the requested poll

    Returns:
        dict: poll data
    """
   
    poll = db[str(interaction.guild.id)]["polls"].get(poll_name)
    if not poll:
        await interaction.response.send_message(f"{poll_name} poll is not found.", ephemeral=True)
    return poll



@poll_group.command(name="reactions")
async def poll_reactions(interaction: Interaction, poll_name: str, options: str, emojis: str=DEFAULT_OPTION_EMOJIS) -> None:
    """Create a poll where message reactions are used to vote

    Args:
        poll_name (str): name of the new poll
        options (str): list of options separated by a comma (,)
        emojis (str): list of emojis to use for voting separated by white space. Defaults to a list of alphabet emojis
    """
    
    # separate option names from emoji (given that they are written in the format: name emoji ....)
    options = [s.strip() for s in options.split(',')]
    # Cut down default emojis to the number of options 
    if emojis == DEFAULT_OPTION_EMOJIS:
        emojis = emojis[:len(options)*2]
    emojis = [PartialEmoji.from_str(emoji) for emoji in emojis.split()]
    if len(options) != len(emojis):
        await interaction.response.send_message("Every option should have an emoji!", ephemeral=True)
        return
    elif not all(emoji.is_unicode_emoji() or emoji.is_custom_emoji() for emoji in emojis):
        await interaction.response.send_message("Invalid emoji!", ephemeral=True)
        return
    elif not (await validate_options(interaction, options) and await validate_options(interaction, emojis)):
        return
    # this check should stay after the validate_options call since validate_options removes duplicates
    elif len(options) != len(emojis):
        await interaction.response.send_message("Duplicate emojis/options are not allowed in polls", ephemeral=True)
        return

    # create and send the poll message
    desc = '\n'.join(
        f"{option:<{MAX_POLL_OPTION_LENGTH}} {emoji}" for option, emoji in zip(options, emojis))
    embed = Embed(title=poll_name, description=desc,  color=Color.blue())
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar)
    await interaction.response.send_message(embed=embed)
    message = await interaction.original_response()
    # react to the sent poll message with all given emojis to make voting easier for members
    for emoji in emojis:
        await message.add_reaction(str(emoji))


@poll_group.command(name="anonymous")
async def poll_anonymous(interaction: Interaction, poll_name: str, options: str, public_results: bool=True) -> None:
    """Create an anonymous poll using view and buttons

    Args:
        poll_name (str): name of the new poll
        options (str): list of options separated by a comma (,)
        public_results (bool): Allow members to view results while the poll is still open. Defaults to True
    """
    
    async def handle_votes(interaction: Interaction, button: Button) -> None:
        """Handles the scores when a vote button is clicked

        Args:
            button (Button): clicked button
        """

        # allow members to vote only once
        poll = await get_poll(interaction, poll_name)
        member_id = interaction.user.id
        if not poll or member_id in poll["voters"]:
            return

        option = button.label
        poll["voters"].append(member_id)
        poll["votes"][option] += 1
        await interaction.response.defer()


    guild_db = db[str(interaction.guild.id)]

    if poll_name.lower() in map(lambda s: s.lower(), guild_db["polls"].keys()):
        await interaction.response.send_message("Poll already exists.", ephemeral=True)
        return

    options = [s.strip() for s in options.split(',')]
    if not await validate_options(interaction, options):
        return

    # create and send poll message
    view = create_menu(options, [handle_votes])

    embed = Embed(title=poll_name, color=Color.blue())
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar)
    embed.add_field(name="status", value="*Open*", inline=False)

    await interaction.response.send_message(embed=embed, view=view)

    # add poll data to the database
    message = await interaction.original_response()
    guild_db["polls"][poll_name] = {
        "voters": [],
        "votes": {option: 0 for option in options},
        "channel_id": interaction.channel.id,
        "message_id": message.id,
        "author_id": interaction.user.id,
        "public_results": public_results
    }


@poll_group.command(name="result")
async def result(interaction: Interaction, poll_name: str) -> None:
    """Send the result of the requested poll (works only for anonymous poll)

    Args:
        poll_name (str): name of the requested poll
    """

    poll = await get_poll(interaction, poll_name)
    if not poll:
        return
    
    # Only send the results if they are public or if the request is from the author or an admin
    if not poll["public_results"] and poll["author_id"] != interaction.user.id and not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("You don't have permission to view results of this poll.", ephemeral=True)
        return

    # load and format votes
    votes = poll["votes"]
    sorted_keys = sorted(votes, key=lambda k: votes[k], reverse=True)
    result_str = "\n".join([f"{k}: {votes[k]}" for k in sorted_keys])
    
    # create and send results message
    embed = Embed(title=f"{poll_name} results",
                  description=result_str, color=Color.green())
    await interaction.response.send_message(embed=embed)


@poll_group.command(name="close")
async def close(interaction: Interaction, poll_name: str) -> None:
    """Close the requested poll (works only for anonymous poll)

    Args:
        poll_name (str): name of the requested poll
    """
    
    poll = await get_poll(interaction, poll_name)
    if not poll:
        return

    # Only allow author and admins to close the poll
    if poll["author_id"] != interaction.user.id and not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("You don't have permission to close polls that you don't own.", ephemeral=True)
        return
    channel = await interaction.guild.fetch_channel(poll["channel_id"])
    message = await channel.fetch_message(poll["message_id"])

    # change the status of the poll message to Closed and change the embed color to red
    embed = message.embeds[0]
    embed.color = Color.dark_red()
    embed.set_field_at(index=len(message.embeds)-1,
                       name="status", value="*Closed*", inline=False)
    await message.edit(view=None, embed=embed)

    # send poll result
    await result.callback(interaction, poll_name)
 
    # delete poll data and confirm that the poll has been closed  
    del db[str(interaction.guild.id)]["polls"][poll_name]
    await interaction.followup.send(f"{poll_name} poll has been closed.")


exported_commands = [poll_group]
