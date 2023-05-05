"""
The module is launched by the admin command.
The weather data is stored in the database.
"""
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from config.config import ADMIN_ID
# from config.config_dev import ADMIN_ID
from handlers.entry_database import writing_row
from lexicon.lexicon import LEXICON_BOTH

router = Router()


@router.message(Command(commands=['admin']), StateFilter(default_state))
async def admin_command(message: Message):
    """
    Works on the /admin command.
    If admin then writes
    weather data in database
    """
    if message.from_user.id == int(ADMIN_ID):
        await writing_row()
    else:
        await message.answer(text=LEXICON_BOTH['error_enter'])


if __name__ == '__main__':
    writing_row()
