from discord import app_commands, Interaction, TextChannel, Permissions, Embed, Color
from replit import db

welcome_event_group = app_commands.Group(name="welcome", description="Configure members welcome event settings", default_permissions=Permissions(manage_guild=True))
welcome_status_group = app_commands.Group(parent=welcome_event_group, name="status", description="Get or change the status of welcome new members")
welcome_channel_group = app_commands.Group(parent=welcome_event_group, name="channel", description="Get or change the welcome test channel")
welcome_messages_group = app_commands.Group(parent=welcome_event_group, name="messages", description="Configure welcome messages")


@welcome_status_group.command(name="get")
@app_commands.checks.has_permissions(manage_guild=True)
async def get_welcome_status(interaction: Interaction) -> None:
    """Send whether welcome new members is active or not
    """

    welcome_new_members = db[str(interaction.guild.id)]["welcome_new_members"]
    await interaction.response.send_message(f"Welcome new members: {welcome_new_members}" )

@welcome_status_group.command(name="set")
@app_commands.checks.has_permissions(manage_guild=True)
async def set_welcome_status(interaction: Interaction, active: bool) -> None:
    """Change the status of welcome new members

    Args:
        active (bool): whether welcome new members is active or not
    """
    
    db[str(interaction.guild.id)]["welcome_new_members"] = active
    await interaction.response.send_message(f"Welcome new members has been updated to: {active}")


@welcome_channel_group.command(name="get")
@app_commands.checks.has_permissions(manage_guild=True)
async def get_welcome_channel(interaction: Interaction) -> None:
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
@app_commands.checks.has_permissions(manage_guild=True)
async def set_welcome_channel(interaction: Interaction, channel: TextChannel) -> None:
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
@app_commands.checks.has_permissions(manage_guild=True)
async def get_welcome_messages(interaction: Interaction) -> None:
    """Send list welcome messages
    """

    # load and format messages
    messages = db[str(interaction.guild.id)]["welcome_messages"]
    messages_str = "\n".join([f"{i}: {msg}" for i, msg in enumerate(messages)])

    # create and send an embed with the messages
    embed = Embed(title="welcome messages", description=messages_str, color=Color.green())
    await interaction.response.send_message(embed=embed)


@welcome_messages_group.command(name="add")
@app_commands.checks.has_permissions(manage_guild=True)
async def add_welcome_messages(interaction: Interaction, message: str) -> None:
    """Add a new welcome message

    Args:
        message (str): Use $USER for mentioning the user and $SERVER for the server name 
    """
    
    # append message to the database
    message = message.strip()
    db[str(interaction.guild.id)]["welcome_messages"].append(message)
    
    await interaction.response.send_message(f"message have been added: {message}")


@welcome_messages_group.command(name="delete")
@app_commands.checks.has_permissions(manage_guild=True)
async def delete_welcome_messages(interaction: Interaction, message_index: int) -> None:
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



exported_commands = [welcome_event_group]