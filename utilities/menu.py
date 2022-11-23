<<<<<<<< HEAD:utils/menu/menu.py
from discord import ButtonStyle
from discord.ui import View, Button
========
from discord import ButtonStyle, Interaction
from discord.ui import Button, View
from collections.abc import Callable
>>>>>>>> c3bd5983da1d1b694590bc7a810c5631e1c4f0dd:utilities/menu.py


def create_menu(labels: list[str], callback_handler: Callable[[Interaction, Button], None], button_styles: list[ButtonStyle] = None) -> View:
    class SuperButton(Button):
        def __init__(self, label, callback, style=ButtonStyle.grey):
            super().__init__(label=label, style=style)
            self.sub_callback = callback

        async def callback(self, interaction):
            await self.sub_callback(interaction, self)

    view = View()
    current_style = ButtonStyle.gray
    for i in range(len(labels)):
        if button_styles != None and i < len(button_styles):
            current_style = button_styles[i]
        button = SuperButton(
            label=labels[i],
            callback=callback_handler,
            style=current_style
        )
        view.add_item(button)
    return view
