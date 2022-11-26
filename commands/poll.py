from discord import Embed, PartialEmoji, Color
from discord.ext import commands
from utils.decorators import command
from constants import MAX_POLL_CHOICES, MAX_POLL_CHOICE_LENGTH
from utils.menu import create_menu
from replit import db


async def validate_choices(ctx: commands.Context, choices: list[str]) -> bool:
    """
        Validates the given choices and sends an error message to the channel if choices are not valid

        Returns: True if choices are valid, False otherwise
    """
    for i in range(len(choices)-1, -1, -1):
        j = choices.index(choices[i])
        if j != i:
            choices.pop(j)

    if len(choices) > MAX_POLL_CHOICES:
        await ctx.send(f"Poll must have at most {MAX_POLL_CHOICES} choices!")
        return False
    elif len(choices) < 2:
        await ctx.send("Poll must have at least 2 choices!")
        return False
    elif type(choices[0]) == str and not all(len(choice) <= MAX_POLL_CHOICE_LENGTH for choice in choices):
        await ctx.send(f"Choice name length must be at most {MAX_POLL_CHOICES} characters!")
        return False

    return True


async def get_poll(ctx: commands.Context, poll_name: str) -> dict:
    """
        Returns the poll data from the database if it exists, otherwise sends an error message to the channel and returns None
    """
    poll = db[ctx.guild.id]["polls"].get(poll_name)
    if not poll:
        await ctx.send(f"{poll_name} poll is not found.")
    return poll


@commands.command(name="poll", help="create a poll")
@command
async def poll(ctx, poll_name, *choices):
    names = list(choices[::2])
    emojis = [PartialEmoji.from_str(emoji) for emoji in choices[1::2]]
    if len(choices) % 2 != 0:
        await ctx.send("Every choice should have an emoji!")
        return
    elif not all(emoji.is_unicode_emoji() or emoji.is_custom_emoji() for emoji in emojis):
        await ctx.send("Invalid emoji!")
        return
    elif not (await validate_choices(ctx, names) and await validate_choices(ctx, emojis)):
        return
    elif len(names) != len(emojis):
        await ctx.send("Duplicate emojis/choices are not allowed in polls")
        return

    desc = '\n'.join(
        f"{name:<{MAX_POLL_CHOICE_LENGTH}} {emoji}" for name, emoji in zip(names, emojis))
    embed = Embed(title=poll_name, description=desc,  color=Color.blue())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
    message = await ctx.send(embed=embed)
    for emoji in emojis:
        await message.add_reaction(str(emoji))


@commands.command(name="poll_auto", help="create a poll")
@command
async def poll_auto(ctx, poll_name, *choices):
    choices = list(choices)
    if not await validate_choices(ctx, choices):
        return

    emoji_a = '🇦'
    emojis = []
    for i in range(len(choices)):
        emoji = chr(ord(emoji_a)+i)
        partial_emoji = PartialEmoji.from_str(emoji)
        emojis.append(str(partial_emoji))
    extended_choices = [[choices[i//2], emojis[i//2]][i % 2 == 1]
                        for i in range(len(choices)*2)]
    await poll(ctx, poll_name, *extended_choices)


@commands.command(name="poll_anonymous", help="create an anonymous poll")
@command
async def poll_anonymous(ctx, poll_name, *choices):
    async def handle_votes(interaction, button):
        poll = guild_db["polls"].get(poll_name, None)
        user_id = interaction.user.id
        if not poll or user_id in poll["voters"]:
            return

        choice = button.label
        poll["voters"].append(user_id)
        poll["votes"][choice] += 1
        await interaction.response.defer()

    guild_db = db[ctx.guild.id]

    if poll_name.lower() in map(lambda s: s.lower(), guild_db["polls"].keys()):
        await ctx.send("Poll already exists.")
        return

    choices = list(choices)
    if not await validate_choices(ctx, choices):
        return

    view = create_menu(choices, [handle_votes])

    embed = Embed(title=poll_name, color=Color.blue())
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
    embed.add_field(name="status", value="*Open*", inline=False)

    message = await ctx.send(embed=embed, view=view)

    guild_db["polls"][poll_name] = {
        "voters": [],
        "votes": {choice: 0 for choice in choices},
        "channel_id": message.channel.id,
        "message_id": message.id,
    }


@commands.command(name="result", help="prints the result of the given poll (works only for anonymous poll)")
@command
async def result(ctx, poll_name):
    poll = await get_poll(ctx, poll_name)
    if not poll:
        return

    votes = poll["votes"]
    sorted_keys = sorted(votes, key=lambda k: votes[k], reverse=True)
    result_str = "\n".join([f"{k}: {votes[k]}" for k in sorted_keys])
    embed = Embed(title=f"{poll_name} results",
                  description=result_str, color=Color.green())
    await ctx.send(embed=embed)


@commands.command(name="close", help="closes the given poll (works only for anonymous poll)")
@command
async def close(ctx, poll_name):
    poll = await get_poll(ctx, poll_name)
    if not poll:
        return

    channel = await ctx.guild.fetch_channel(poll["channel_id"])
    message = await channel.fetch_message(poll["message_id"])

    embed = message.embeds[0]
    embed.color = Color.dark_red()
    embed.set_field_at(index=len(message.embeds)-1,
                       name="status", value="*Closed*", inline=False)
    await message.edit(view=None, embed=embed)

    await result(ctx, poll_name)
    del db[ctx.guild.id]["polls"][poll_name]
    await ctx.send(f"{poll_name} poll has been closed.")


exported_commands = [poll, poll_auto, poll_anonymous, result, close]
