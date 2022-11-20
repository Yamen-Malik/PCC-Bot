import discord


class MajorMenu(discord.ui.View):
    def __init__(self, member):
        self.member = member
        super().__init__()

    async def choose_major(self, major, interaction):
        member = self.member if self.member else interaction.user
        majors = {
            "CS": "computer science",
            "SE": "software engineering",
            "IS": "cyber security",
            "AI": "artificial intelligence",
        }
        major = majors.get(major, "")
        try:
            new_role = filter(lambda r: r.name.lower() ==
                              major, member.guild.roles).__next__()
            for role in member.roles:
                if role.name.lower() in majors.values():
                    await member.remove_roles(role)
                    break
            await member.add_roles(new_role)
            await interaction.message.delete()
        except StopIteration:
            await interaction.channel.send(f"Failed to set role: role not available")

    @discord.ui.button(label="Computer Science", style=discord.ButtonStyle.primary)
    async def CS_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.choose_major("CS", interaction)

    @discord.ui.button(label="Software Engineering", style=discord.ButtonStyle.success)
    async def SE_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.choose_major("SE", interaction)

    @discord.ui.button(label="Cyber Security", style=discord.ButtonStyle.danger)
    async def IS_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.choose_major("IS", interaction)

    @discord.ui.button(label="Artificial Intelligence", style=discord.ButtonStyle.secondary)
    async def AI_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.choose_major("AI", interaction)
