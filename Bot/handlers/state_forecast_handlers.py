"""
Handlers FSM forecast
"""

from aiogram import Router
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from database.postgresessions import session_number_rows, session_get_coordinates, session_get_language
from handlers.state_settings_handlers import engine
from keyboards.inline_keyboards import create_inline_kb
from lexicon.lexicon import LEXICON_BOTH
from lexicon.symbols_weather import SYMBOLS
from state.states import FSMForecast
from utils.parsing_data import parse_forecast

router = Router()


##################### Start FSM on command /forecast ######################################################

@router.message(Command(commands=['forecast']), StateFilter(default_state))
async def forecast_command(message: Message, state: FSMContext):
    """
    Fires on the /forecast command in the default state.
    If the user and his coordinates are in the database, the bot translates
    to the state of waiting for the selection of the day for the forecast.
    Otherwise, it prompts you to fill in the settings.
    """
    user_id = message.from_user.id

    if session_number_rows(engine, user_id) and session_get_coordinates(engine, user_id) is not None:

        # We extract the language from the user profile
        lang = session_get_language(engine, user_id)
        if lang == 'ru':
            from lexicon.lexicon_ru import LEXICON
            # Create an inline clave to select a day
            keyboards = create_inline_kb(width=1, Сегодня=0, Завтра=1, Послезавтра=2)
        else:
            from lexicon.lexicon_en import LEXICON
            keyboards = create_inline_kb(width=1, Today=0, Tomorrow=1, Day_after_tomorrow=2)

        await message.answer(text=LEXICON['day_select'], reply_markup=keyboards)

        # Set the pending state of the selection
        await state.set_state(FSMForecast.select_forecast)
    else:
        await message.answer(text=LEXICON_BOTH['error'])
        await state.clear()


@router.callback_query(StateFilter(FSMForecast.select_forecast), Text(text=['0', '1', '2']))
async def today_press(callback: CallbackQuery, state: FSMContext):
    """
    It works on the day selection buttons, displays the forecast
    on the corresponding day, stops the FSM
    """
    # Delete message with buttons
    await callback.message.delete()

    user_id = callback.message.chat.id

    # We extract the language from the user profile
    lang = session_get_language(engine, user_id)
    if lang == 'ru':
        from lexicon.lexicon_ru import INDICATORS, UNIT
    else:
        from lexicon.lexicon_en import INDICATORS, UNIT

    weather = parse_forecast(session_get_coordinates(engine, user_id), lang)[int(callback.data)]

    await callback.message.answer(text=
                                  f'{weather["date_time"]}\n'
                                  f'{INDICATORS["maxtemp"]}{weather["maxtemp_c"]} \u00b0С\n'
                                  f'{INDICATORS["mintemp"]}{weather["mintemp_c"]} \u00b0С\n'
                                  f'{weather["condition"]}    {SYMBOLS[weather["code"]]}\n'
                                  f'{INDICATORS["maxwind"]}{weather["maxwind_kph"]} {UNIT["mps"]}\n'
                                  f'{INDICATORS["avghumidity"]}{weather["avghumidity"]} %\n'
                                  f'{INDICATORS["precip"]}{weather["totalprecip_mm"]} {UNIT["mm"]}\n')

    await state.clear()


@router.message(StateFilter(FSMForecast.select_forecast))
async def warning_not_forecast(message: Message):
    """
    If something incorrect is sent when selecting a day
    """
    user_id = message.from_user.id

    # We extract the language from the user profile
    lang = session_get_language(engine, user_id)
    if lang == 'ru':
        from lexicon.lexicon_ru import LEXICON
    else:
        from lexicon.lexicon_en import LEXICON
    await message.answer(text=LEXICON['incorrect'])
