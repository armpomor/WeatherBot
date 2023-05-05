from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_inline_kb(width: int,
                     last_btn: str | None = None,
                     **kwargs: [str, str]) -> InlineKeyboardMarkup:
    """
    Inline Keyboard Generator
    The input takes the width parameter, named parameters (keys / values)
    from which you can form inline buttons. The key is the name of the button,
    value - data. The function optionally adds the last button,
    if the last_btn argument is passed.
    Returns an inline keyboard object.
    """
    # Builder initialization
    kb_builder = InlineKeyboardBuilder()
    # List initialization for buttons
    buttons = []

    # Filling the list with buttons from kwargs
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=text))

    # Unpack the list with buttons into the builder using the row method with the width parameter
    kb_builder.row(*buttons, width=width)

    # Add the last button to the builder if it is passed to the function
    if last_btn:
        kb_builder.row(InlineKeyboardButton(
            text=last_btn,
            callback_data='last_btn'))

    return kb_builder.as_markup()
