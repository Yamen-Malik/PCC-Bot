from discord.ext import commands
from discord import Embed, Color
from utils.decorators import command
import requests


@commands.command(name="quote", help="Returns a programming related quote by it's id, if id isn't provided return random quote")
@command
async def quote(ctx: commands.Context, id: str = "random") -> bool:
    try:
        # send GET request to programming quotes api
        content = requests.get(
            f"https://programming-quotes-api.herokuapp.com/Quotes/{id}")
        if content.status_code == 404:
            await ctx.send("Invalid quote id")
            return False
        elif content.status_code != 200:
            raise Exception

        # load response and send it's content in an Embed object
        content = content.json()
        quote = Embed(
            title=content["author"], description=content["en"]+"\n\n"+content['id'], color=Color.gold())
        await ctx.send(embed=quote)
        return True
    except:
        await ctx.send("Error while requesting quote")
        return False

exported_commands = [quote]
