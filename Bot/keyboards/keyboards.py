from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def local_kb():
    """
    Button Locale
    """
    kb_builder = ReplyKeyboardBuilder()
    btn = KeyboardButton(text='Locale', request_location=True)
    kb_builder.add(btn)

    return kb_builder.as_markup(resize_keyboard=True)
