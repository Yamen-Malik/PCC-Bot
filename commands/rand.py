from discord.ext import commands
from commands.decorators import command
import random


@commands.command(name="rand", help="Generate a random number in the given range [l, u)")
@command
async def rand(ctx, l=0, u=1):
    try:
        l = int(l)
        u = int(u)
    except ValueError:
        print("Invalid lower/upper value")
        return
    if l > u:
        l, u = u, l
    await ctx.send(random.random()*abs(u-l)+min(l, u))


@commands.command(name="randint", help="Generate a random integer in the given range [l, u]")
@command
async def randint(ctx, l=0, u=100):
    try:
        l = int(l)
        u = int(u)
    except ValueError:
        print("Invalid lower/upper value")
        return
    if l > u:
        l, u = u, l
    await ctx.send(random.randint(l, u))


@commands.command(name="randchoice", help="Returns a random value from the given values")
@command
async def randchoice(ctx, *args):
    if not args:
        return
    await ctx.send(random.choice(args))


@commands.command(name="randuser", help="Mentions a random member from the channel or the whole server if true is passed")
@command
async def randuser(ctx, server_wide=False):
    if server_wide and server_wide.lower() == "true":
        members = ctx.guild.members
    else:
        members = ctx.channel.members
    await ctx.send(random.choice(members).mention)
