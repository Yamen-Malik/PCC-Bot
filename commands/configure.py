from discord import app_commands, Interaction, TextChannel, Embed, Color
from discord.ext.commands import Bot
from replit import db


@app_commands.guild_only()
@app_commands.default_permissions(manage_guild=True)
class Welcome(app_commands.Group):
    """Configure members welcome event settings
    """
    welcome_status_group = app_commands.Group(name="status", description="Get or change the status of welcome new members")
    welcome_channel_group = app_commands.Group(name="channel", description="Get or change the welcome test channel")
    welcome_messages_group = app_commands.Group(name="messages", description="Configure welcome messages")

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        super().__init__()


    @welcome_status_group.command(name="get")
    async def get_welcome_status(self, interaction: Interaction) -> None:
        """Send whether welcome new members is active or not
        """

        welcome_new_members = db[str(interaction.guild.id)]["welcome_new_members"]
        await interaction.response.send_message(f"Welcome new members: {welcome_new_members}" )

    @welcome_status_group.command(name="set")
    async def set_welcome_status(self, interaction: Interaction, active: bool) -> None:
        """Change the status of welcome new members

        Args:
            active (bool): whether welcome new members is active or not
        """
        
        db[str(interaction.guild.id)]["welcome_new_members"] = active
        await interaction.response.send_message(f"Welcome new members has been updated to: {active}")



    @welcome_channel_group.command(name="get")
    async def get_welcome_channel(self, interaction: Interaction) -> None:
        """Send the current welcome channel name
        """

        guild_db = db[str(interaction.guild.id)]
        channel = None
        for ch in interaction.guild.channels:
            if ch.name.lower() == guild_db["welcome_channel"]:
                channel = ch
                break
        
        if not channel:
            await interaction.response.send_message("Welcome channel: NONE")
            return

        await interaction.response.send_message(f"Welcome channel: {channel.mention}")


    @welcome_channel_group.command(name="set")
    async def set_welcome_channel(self, interaction: Interaction, channel: TextChannel) -> None:
        """Change the current welcome channel

        Args:
            channel (TextChannel): the new welcome text channel
        """

        if type(channel) != TextChannel:
            await interaction.response.send_message("Invalid channel", ephemeral=True)
            return
        
        db[str(interaction.guild.id)]["welcome_channel"] = channel.name.lower()
        await interaction.response.send_message(f"welcome channel has been updated to: {channel.name}")



    @welcome_messages_group.command(name="get")
    async def get_welcome_messages(self, interaction: Interaction) -> None:
        """Send list welcome messages
        """

        # load and format messages
        messages = db[str(interaction.guild.id)]["welcome_messages"]
        messages_str = "\n".join([f"{i}: {msg}" for i, msg in enumerate(messages)])

        # create and send an embed with the messages
        embed = Embed(title="welcome messages", description=messages_str, color=Color.green())
        await interaction.response.send_message(embed=embed)


    @welcome_messages_group.command(name="add")
    async def add_welcome_messages(self, interaction: Interaction, message: str) -> None:
        """Add a new welcome message

        Args:
            message (str): Use $USER for mentioning the user and $SERVER for the server name 
        """
        
        # append message to the database
        message = message.strip()
        db[str(interaction.guild.id)]["welcome_messages"].append(message)
        
        await interaction.response.send_message(f"message have been added: {message}")


    @welcome_messages_group.command(name="delete")
    async def delete_welcome_messages(self, interaction: Interaction, message_index: int) -> None:
        """Delete am existing welcome message

        Args:
            message_index (int): the index of the message. Use messages get command to view indices
        """

        # validate index
        if message_index < 0 or message_index >= len(db[str(interaction.guild.id)]["welcome_messages"]):
            await interaction.response.send_message(f"Invalid message index", ephemeral=True)
            return

        # delete message
        deleted_message = db[str(interaction.guild.id)]["welcome_messages"].pop(message_index)
        await interaction.response.send_message(f"Message have been deleted: {deleted_message}")


async def setup(bot: Bot) -> None:
    bot.tree.add_command(Welcome(bot))