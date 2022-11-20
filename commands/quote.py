from discord.ext import commands
from discord import Embed
from commands.decorators import command
import requests


@commands.command(name="quote", help="Returns a programming related quote by it's id, if id isn't provided return random quote")
@command
async def quote(ctx, id="random"):
    try:
        content = requests.get(
            f"https://programming-quotes-api.herokuapp.com/Quotes/{id}")
        if content.status_code == 404:
            await ctx.send("Invalid quote id")
            return
        elif content.status_code != 200:
            raise Exception

        content = content.json()
        quote = Embed(
            title=content["author"], description=content["en"]+"\n\n"+content['id'], color=0xd10a07)
        await ctx.send(embed=quote)
    except:
        await ctx.send("Error while requesting quote")
