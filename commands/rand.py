from discord.ext import commands
from utils.decorators import command
import random


async def send_rand(ctx: commands.Context, l, u, is_int: bool) -> None:
    """
    Generates and sends a random number in the given range
    
    Sends an error message if the range isn't valid
    """
    try:
        l = float(l)
        u = float(u)
        if l > u:
            l, u = u, l
        
        result = random.randint(l, u) if is_int else random.uniform(u, l)
    except ValueError:
        await ctx.send("Invalid lower or upper value")
        return
    
    await ctx.send(result)

@commands.command(name="rand", help="Generate a random number in the given range [l, u)")
@command
async def rand(ctx: commands.Context, l: int = 0, u: int = 1):
    await send_rand(ctx, l, u, False)

@commands.command(name="rand_int", help="Generate a random integer in the given range [l, u]")
@command
async def rand_int(ctx: commands.Context, l: int = 0, u: int = 100):
    await send_rand(ctx, l, u, True)


@commands.command(name="rand_choice", help="Returns a random value from the given values")
@command
async def rand_choice(ctx: commands.Context, *args: tuple[str]):
    if not args:
        return
    await ctx.send(random.choice(args))


@commands.command(name="rand_user", help="Mentions a random member from the channel or the whole server if true is passed")
@command
async def rand_user(ctx: commands.Context, server_wide: bool = False):
    if server_wide and server_wide.lower() == "true":
        members = ctx.guild.members
    else:
        members = ctx.channel.members
    await ctx.send(random.choice(members).mention)

exported_commands = [rand, rand_int, rand_choice, rand_user]
