"""
Handlers FSM settings
"""

from aiogram import Router, F
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from database.postgresessions import connect_db, session_add, session_update_settings, session_number_rows, \
    session_get_language
from keyboards.inline_keyboards import create_inline_kb
from keyboards.keyboards import local_kb
from lexicon.lexicon import LEXICON_BOTH
from state.states import FSMSettings
from utils.utilities import get_ip_data

router = Router()

# Connecting to the database, creating tables and engine
engine = connect_db()


@router.message(Command(commands='stop'), ~StateFilter(default_state))
async def stop_command_state(message: Message, state: FSMContext):
    """
    This handler will respond to the "/stop" command in any state,
    other than the default state, and turn off the state machine,
    those. cancel data entry
    """
    await message.answer(text=LEXICON_BOTH['stop'])
    # Reset the state
    await state.clear()


##################### Start FSM on command /settings ######################################################

@router.message(Command(commands='settings'), StateFilter(default_state))
async def settings_command(message: Message, state: FSMContext):
    """
    This handler will fire on the /settings command in the state
    by default and put the bot in a state of waiting for the choice of language
    """
    # Create an inline clave to select a language
    keyboards = create_inline_kb(width=1, Русский='ru', English='en')
    await message.answer(text=LEXICON_BOTH['lang'], reply_markup=keyboards)

    # Set the language selection wait state
    await state.set_state(FSMSettings.set_language)


@router.callback_query(StateFilter(FSMSettings.set_language), Text(text=['ru', 'en']))
async def language_press(callback: CallbackQuery, state: FSMContext):
    """
    The handler is triggered by pressing a button when choosing a language and translates
    to the input state of the device. Save the response (callback.data of the pressed button)
    in storage by lang key. Using the user_id key, we store the user id.
    By the key name first_name of the user.
    """
    await state.update_data(language=callback.data)
    await state.update_data(user_id=callback.message.chat.id)
    await state.update_data(name=callback.message.chat.first_name)

    lang = callback.data

    # We store the transferred data in the user variable
    user = await state.get_data()

    # We check if the user has no records in the database,
    # then we save the data, and if there is then update
    user_id = callback.message.chat.id
    if session_number_rows(engine, user_id):
        session_update_settings(engine, user, user_id)
    else:
        session_add(user, engine)

    # We delete the message with the buttons, because the next step is the choice of the device
    await callback.message.delete()

    if lang == 'ru':
        from lexicon.lexicon_ru import LEXICON
        # Create an inline keyboard to select a device
        keyboards = create_inline_kb(width=1, Telegram_на_компьютере='Desktop', Мобильное_приложение='Mobile')
    else:
        from lexicon.lexicon_en import LEXICON
        keyboards = create_inline_kb(width=1, Telegram_Desktop='Desktop', Mobile_app='Mobile')

    await callback.message.answer(text=LEXICON['select_device'], reply_markup=keyboards)

    # Set the waiting state for device selection
    await state.set_state(FSMSettings.set_device)


@router.message(StateFilter(FSMSettings.set_language))
async def warning_not_lang(message: Message):
    """
    If something incorrect is sent when choosing a language
    """
    await message.answer(text=LEXICON_BOTH['incorrect_lang'])


@router.callback_query(StateFilter(FSMSettings.set_device), Text(text='Desktop'))
async def device_press(callback: CallbackQuery, state: FSMContext):
    """
    Fires if the user is using Telegram_Desktop.
    Then set the coordinates by IP
    """
    # Delete message with buttons
    await callback.message.delete()

    coordinates = get_ip_data()['loc']

    await state.update_data(coordinates=coordinates)

    # We store the transferred data in the user variable
    user = await state.get_data()

    # We check if the user has no records in the database,
    # then we save the data, and if there is then update
    user_id = callback.message.chat.id
    if session_number_rows(engine, user_id):
        session_update_settings(engine, user, user_id)
    else:
        session_add(user, engine)

    # We extract the language from the user profile
    lang = session_get_language(engine, user_id)
    if lang == 'ru':
        from lexicon.lexicon_ru import LEXICON
    else:
        from lexicon.lexicon_en import LEXICON

    await callback.message.answer(text=LEXICON['completed_settings'])

    await state.clear()


@router.callback_query(StateFilter(FSMSettings.set_device), Text(text='Mobile'))
async def device_press(callback: CallbackQuery, state: FSMContext):
    """
    Fires if the user is using Telegram_Mobile.
    Sending a button to determine the geolocation
    """
    # Delete message with buttons
    await callback.message.delete()

    user_id = callback.message.chat.id

    # We extract the language from the user profile
    lang = session_get_language(engine, user_id)
    if lang == 'ru':
        from lexicon.lexicon_ru import LEXICON
    else:
        from lexicon.lexicon_en import LEXICON

    await callback.message.answer(text=LEXICON['locale'], reply_markup=local_kb())

    # Set the state of waiting for the input of the location
    await state.set_state(FSMSettings.set_location)


@router.message(StateFilter(FSMSettings.set_device))
async def warning_not_device(message: Message):
    """
    If something incorrect is sent when choosing a device
    """
    user_id = message.from_user.id

    # We extract the language from the user profile
    lang = session_get_language(engine, user_id)
    if lang == 'ru':
        from lexicon.lexicon_ru import LEXICON
    else:
        from lexicon.lexicon_en import LEXICON

    await message.answer(text=LEXICON['incorrect'])


@router.message(F.location)
async def set_location(message: Message, state: FSMContext):
    await state.update_data(coordinates=f'{message.location.latitude},{message.location.longitude}')

    # We store the transferred data in the user variable
    user = await state.get_data()

    # We check if the user has no records in the database,
    # then we save the data, and if there is then update
    user_id = message.from_user.id
    if session_number_rows(engine, user_id):
        session_update_settings(engine, user, user_id)
    else:
        session_add(user, engine)

    # We extract the language from the user profile
    lang = session_get_language(engine, user_id)
    if lang == 'ru':
        from lexicon.lexicon_ru import LEXICON
    else:
        from lexicon.lexicon_en import LEXICON

    await message.answer(text=LEXICON['completed_settings'], reply_markup=ReplyKeyboardRemove())

    await state.clear()


@router.message(StateFilter(FSMSettings.set_location))
async def warning_not_location(message: Message):
    """
   If something incorrect is sent when sending the location
    """
    user_id = message.from_user.id

    # We extract the language from the user profile
    lang = session_get_language(engine, user_id)
    if lang == 'ru':
        from lexicon.lexicon_ru import LEXICON
    else:
        from lexicon.lexicon_en import LEXICON

    await message.answer(text=LEXICON['incorrect_locale'])
