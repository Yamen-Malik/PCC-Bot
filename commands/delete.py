from discord import app_commands, Interaction


@app_commands.command(name="delete")
@app_commands.checks.has_permissions(manage_messages=True)
async def delete(interaction: Interaction, n: int,) -> None:
    """Delete last n messages in this channel

    Args:
        n (int): number of messages to delete
    """
    
    try:
        assert type(n) == int
        await interaction.response.send_message(f"Deleting {n} message{'s'*(n>1)}", ephemeral=True)
        await interaction.channel.purge(limit=n)
    except AssertionError:
        await interaction.response.send_message("Invalid delete argument.", ephemeral=True)
    except:
        await interaction.response.send_message("Error occurred while deleting the messages", ephemeral=True)

exported_commands = [delete]
