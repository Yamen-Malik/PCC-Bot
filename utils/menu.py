from collections.abc import Callable

from discord import ButtonStyle, Interaction
from discord.ui import Button, View


def create_menu(
    labels: list[str],
    callback_handlers: list[Callable[[Interaction, Button], None]],
    button_styles: list[ButtonStyle] = None,
) -> View:
    class SuperButton(Button):
        def __init__(self, label, callback, style=ButtonStyle.grey):
            super().__init__(label=label, style=style)
            self.sub_callback = callback

        async def callback(self, interaction):
            await self.sub_callback(interaction, self)

    view = View()
    current_style = ButtonStyle.gray
    for i, label in enumerate(labels):
        if button_styles is not None and i < len(button_styles):
            current_style = button_styles[i]
        button = SuperButton(
            label=label,
            callback=callback_handlers[i % len(callback_handlers)],
            style=current_style,
        )
        view.add_item(button)
    return view
