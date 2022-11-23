from discord import ButtonStyle
from discord.ui import View, Button


def create_menu(labels, methods, button_styles=None):
    class SuperButton(Button):
        def __init__(self, label, callback, style=ButtonStyle.grey):
            super().__init__(label=label, style=style)
            self.sub_callback = callback

        async def callback(self, interaction):
            await self.sub_callback(interaction, self)
    view = View()
    current_style = ButtonStyle.gray
    for i in range(len(labels)):
        if button_styles != None:
            current_style = button_styles[i]
        button = SuperButton(
            label=labels[i],
            callback=methods[i],
            style=current_style
        )
        view.add_item(button)
    return view
