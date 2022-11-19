import discord
from discord.ext import commands
from keep_alive import keep_alive
from replit import db
from constants import *
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(intents=intents, command_prefix=COMMAND_CHAR, case_insensitive=True)


class MajorMenu(discord.ui.View):
    def __init__(self, member):
        self.member = member
        super().__init__()
    
    async def choose_major(self, major, interaction):
        member = self.member if self.member else interaction.user
        majors = {
            "CS":"computer science",
            "SE":"software engineering",
            "IS":"cyber security",
            "AI":"artificial intelligence",
        }
        major = majors.get(major, "")
        try:
            new_role = filter(lambda r: r.name.lower()==major, member.guild.roles).__next__()
            for role in member.roles:
                if role.name.lower() in majors.values():
                    await member.remove_roles(role)
                    break
            await member.add_roles(new_role)
            await interaction.message.delete()
        except StopIteration: 
            await interaction.channel.send(f"Failed to set role: role not available")

    @discord.ui.button(label="Computer Science",style=discord.ButtonStyle.primary)
    async def CS_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.choose_major("CS", interaction)
    
    @discord.ui.button(label="Software Engineering",style=discord.ButtonStyle.success)
    async def SE_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.choose_major("SE",interaction)
    
    @discord.ui.button(label="Cyber Security",style=discord.ButtonStyle.danger)
    async def IS_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.choose_major("IS", interaction)
    
    @discord.ui.button(label="Artificial Intelligence",style=discord.ButtonStyle.secondary)
    async def AI_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.choose_major("AI", interaction)


def get_command_data(command:str):
    commands = db.get("commands",{})
    commands[command] = commands.get(command, default_command_data)
    db["commands"] = commands
    return commands[command]
    
def command(func):
    async def wrapper(ctx, *args, **kwargs):
        data = get_command_data(func.__name__)
        if data["active"] and data["is_blacklist"] != (ctx.channel.name.lower() in data["channels"]):
            if all([getattr(ctx.permissions, perm) for perm in data["permissions"]]):
                return await func(ctx, *args, **kwargs)
            else:
                await ctx.send(f"Missing Permissions to run {func.__name__}")
    return wrapper

def edit_command(func):
    async def wrapper(ctx, command, *args, **kwargs):
        if command in map(lambda c:c.name, bot.commands):
            data = get_command_data(command)
            return await func(ctx, command, data, *args, **kwargs)
        else:
            print(f"{command} is not a command")

    return wrapper

@bot.event
async def on_ready():
    print(f"Running as {bot.user}")

@bot.event
async def on_member_join(member):
    if not db["welcome_new_members"]:
        return
    for channel in member.guild.channels:
        if channel.name == db["welcome_channel"]:
            await channel.send(random.choice(db["welcome_messages"]).format(member.mention, member.guild.name))
            view = MajorMenu(member)
            await member.send(f"Select your major", view=view)
            break

@bot.command(name="hello", help="Say hello to the bot")
@command
async def hello(ctx):
    await ctx.send("Hi.")

@bot.command(name="disable", help="Disable one of the bot commands")
@edit_command
@command
async def disable(ctx, command, command_data):
    command_data["active"] = False
    await ctx.send(f"{command} is disabled")

@bot.command(name="enable", help="Enable one of the bot commands")
@edit_command
@command
async def enable(ctx, command, command_data):
    command_data["active"] = True
    await ctx.send(f"{command} is enabled")

@bot.command(name="change_major", help="Change your major role")
@command
async def change_major(ctx):
    menu = MajorMenu(None)
    await ctx.send("Choose major:", view=menu)

@bot.command(name="delete",help="Delete last n messages")
@command
async def delete(ctx, x):
    try:
        member_id = n = None
        if x.startswith("<"):
            member_id = int(x[2:-1])
        else:
            n = int(x)
        
        if member_id:
            await ctx.channel.purge(check=lambda m: m.author.id==member_id)
        else:
            await ctx.channel.purge(limit=n+1)
    except:
        print("Invalid delete argument")

keep_alive()
bot.run(TOKEN)