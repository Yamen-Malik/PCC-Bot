from discord import ButtonStyle, Member
from discord.ext.commands import Cog, Bot
from utils.menu import create_menu
from utils.choose_role import choose_role
from replit import db
from constants import USER_MENTION, SERVER_MENTION
import random
from logging import getLogger


class OnMemberJoin(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = getLogger(__name__)


    @Cog.listener()
    async def on_member_join(self, member: Member):
        guild = member.guild
        self.logger.debug(f"New member joined. Member({member.name}, {member.id}), Guild({guild.name}, {guild.id})")
        
        guild_db = db[str(guild.id)]
        if not guild_db["welcome_new_members"]:
            return

        channel = None
        for ch in guild.channels:
            if ch.name.lower() == guild_db["welcome_channel"].lower():
                channel = ch
                break

        if not channel:
            self.logger.debug("Welcome channel is not found.")
            return

        message = random.choice(guild_db["welcome_messages"])
        message = message.replace(USER_MENTION, member.mention)
        message = message.replace(SERVER_MENTION, guild.name)
        await channel.send(message)

        if len(guild_db["new_member_roles"]) > 1:
            self.logger.debug("Sending role selection view.")
            view = create_menu(
                guild_db["new_member_roles"],
                [choose_role],
                [ButtonStyle.primary, ButtonStyle.success,
                ButtonStyle.danger, ButtonStyle.gray]
            )
            await channel.send(f"Select your major", view=view)
        elif len(guild_db["new_member_roles"]) == 1:
            role_name = guild_db["new_member_roles"][0].lower()
            for role in guild.roles:
                if role.name.lower() == role_name:
                    self.logger.debug(f"Giving member {role.name} role.")
                    await member.add_roles(role)
                    break


async def setup(bot: Bot) -> None:
    await bot.add_cog(OnMemberJoin(bot))