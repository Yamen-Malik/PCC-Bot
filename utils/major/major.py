from discord import Interaction, Button


async def choose_major(interaction: Interaction, button: Button):
    member = interaction.user
    major = button.label
    role = None
    for r in member.guild.roles:
        if r.name.lower() == major.lower():
            role = r
    if role:
        await member.add_roles(role)
        await interaction.channel.send(f"{member.mention} your role now is {major}")
        await interaction.message.delete()
    else:
        await interaction.channel.send(f'failed to change role')
