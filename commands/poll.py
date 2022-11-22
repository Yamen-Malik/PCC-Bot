from discord import Embed, PartialEmoji
from discord.ext import commands
from utilities.decorators import command
from constants import MAX_POLL_CHOICES, MAX_POLL_NAME_LENGTH
from replit import db


@commands.command(name="poll", help="create a poll")
@command
async def poll(ctx, poll_name, *choices):
	names = choices[::2]
	emojis = [PartialEmoji.from_str(emoji) for emoji in choices[1::2]]
	if len(choices) % 2 != 0:
		await ctx.channel.send("Every choice should have an emoji!")
		return
	elif len(choices)//2 > MAX_POLL_CHOICES:
		await ctx.channel.send("Max poll choices exceeded!")
		return
	elif not all(len(name) <= MAX_POLL_NAME_LENGTH for name in names):
		await ctx.channel.send("Choice name length exceeded!")
		return
	elif not all(emoji.is_unicode_emoji() or emoji.is_custom_emoji() for emoji in emojis):
		await ctx.channel.send("Invalid emoji!")
		return
	desc = '\n'.join(
		f"{name:<{MAX_POLL_NAME_LENGTH}} {emoji}" for name, emoji in zip(names, emojis))
	embed = Embed(title=poll_name, description=desc,  color=0xd10a07)
	embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar)
	message = await ctx.channel.send(embed=embed)
	for emoji in emojis:
		await message.add_reaction(str(emoji))

# BUG poll do raise an Unknown Emoji Exception when receiving generated emojis
@commands.command(name="poll_auto", help="create a poll")
@command
async def poll_auto(ctx, poll_name, *choices):
	names = choices
	if len(choices) > MAX_POLL_CHOICES:
		await ctx.channel.send("Max poll choices exceeded!")
		return
	elif not all(len(name) <= MAX_POLL_NAME_LENGTH for name in names):
		await ctx.channel.send("Choice name length exceeded!")
		return
	letter_emoji = ':regional_indicator_{letter}:'
	emojis = [letter_emoji.format(letter=(chr(ord('a')+i)))
			  for i in range(len(choices))]
	print(emojis)
	extended_choices = [[names[i//2], emojis[i//2]][i % 2 == 1]
						for i in range(len(names)*2)]
	await poll(ctx, poll_name, *extended_choices)

# TODO
@commands.command(name="poll_anonymous", help="create an anonymous poll")
@command
async def poll_anonymous(ctx, poll_name, *choices):
	pass

@commands.command(name="result", help="result of all polls")
@command
async def result(ctx):
	await ctx.send(str(db["polls"]))
