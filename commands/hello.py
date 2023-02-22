from discord import app_commands, Interaction

@app_commands.command(name="hello")
async def hello(interaction: Interaction) -> None:
    """Say hello to the bot
    """

    await interaction.response.send_message(f"Hi {interaction.user.mention}.", ephemeral=True)

exported_commands = [hello]
