from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message

from prettytable import PrettyTable

from config.air_gases import CIRCLE_COLOR
from database.postgresessions import session_number_rows, session_get_coordinates, session_get_language
from handlers.state_settings_handlers import engine
from lexicon.lexicon import LEXICON_BOTH
from lexicon.symbols_weather import SYMBOLS
from utils.parsing_data import parse_real_time, parse_astro, parse_air_quality
from utils.utilities import set_color_air

router = Router()


@router.message(Command(commands=["start"]), StateFilter(default_state))
async def start_command(message: Message):
    await message.answer(text=LEXICON_BOTH['start'])


@router.message(Command(commands=['realtime']), StateFilter(default_state))
async def realtime_command(message: Message):
    """
    Triggered by the /realtime command and
    sends the user the current weather,
    if the user and his coordinates are in the database.
    Otherwise, it prompts you to fill in the settings.
    """
    user_id = message.from_user.id

    if session_number_rows(engine, user_id) and session_get_coordinates(engine, user_id) is not None:
        # We extract the language from the user profile
        lang = session_get_language(engine, user_id)
        if lang == 'ru':
            from lexicon.lexicon_ru import INDICATORS, UNIT
        else:
            from lexicon.lexicon_en import INDICATORS, UNIT

        weather = parse_real_time(session_get_coordinates(engine, user_id), lang)
        astro = parse_astro(session_get_coordinates(engine, user_id))

        await message.answer(text=
                             f'{INDICATORS["temp"]}{weather["temp"]} \u00b0С\n'
                             f'{weather["condition"]}    {SYMBOLS[weather["code"]]}\n'
                             f'{INDICATORS["wind_dir"]}{weather["wind_dir"]}\n'
                             f'{INDICATORS["wind"]}{weather["wind_mps"]} {UNIT["mps"]}\n'
                             f'{INDICATORS["humidity"]}{weather["humidity"]} %\n'
                             f'{INDICATORS["precip"]}{weather["precip_mm"]} {UNIT["mm"]}\n'
                             f'{INDICATORS["pressure"]}{weather["pressure_mb"]} {UNIT["pressure"]}\n'
                             f'{INDICATORS["cloud"]}{weather["cloud"]} %\n'
                             f'{INDICATORS["sunrise"]}{astro["sunrise"]}\n'
                             f'{INDICATORS["sunset"]}{astro["sunset"]}\n'
                             f'{INDICATORS["day_long"]}{astro["long_day"]}')
    else:
        await message.answer(text=LEXICON_BOTH['error'])


@router.message(Command(commands=['air_quality']), StateFilter(default_state))
async def air_quality_command(message: Message):
    """
    Triggered by the /air_quality command and
    sends user air quality indicators
    at the moment if user and his coordinates
    is in the database. Otherwise, it prompts you to fill in the settings.
    """
    user_id = message.from_user.id

    if session_number_rows(engine, user_id) and session_get_coordinates(engine, user_id) is not None:
        air = parse_air_quality(session_get_coordinates(engine, user_id))

        # Forming a table for the message
        table = PrettyTable(header=False, align="l", border=False, padding_width=3)

        table.add_row(['CO', f'  {air["CO"]}', 'μg/m\u00B3', f'{CIRCLE_COLOR[set_color_air(air["CO"], "CO")]}'])
        table.add_row(['NO\u00B2', f' {air["NO2"]}', '  μg/m\u00B3', f'  {CIRCLE_COLOR[set_color_air(air["NO2"], "NO2")]}'])
        table.add_row(['O\u00B3', f'  {air["O3"]}', '   μg/m\u00B3', f'   {CIRCLE_COLOR[set_color_air(air["O3"], "O3")]}'])
        table.add_row(['SO\u00B2', f'  {air["SO2"]}', '   μg/m\u00B3', f'   {CIRCLE_COLOR[set_color_air(air["SO2"], "SO2")]}'])
        table.add_row(['pm 2.5', f'{air["pm2_5"]}', 'μg/m\u00B3', f'{CIRCLE_COLOR[set_color_air(air["pm2_5"], "pm2_5")]}'])
        table.add_row(['pm 10', f'{air["pm10"]}', 'μg/m\u00B3', f'{CIRCLE_COLOR[set_color_air(air["pm10"], "pm10")]}'])

        await message.answer(text=f'Good {CIRCLE_COLOR["green"]}{CIRCLE_COLOR["yellow"]}{CIRCLE_COLOR["orange"]}'
                                  f'{CIRCLE_COLOR["brown"]}{CIRCLE_COLOR["purple"]}{CIRCLE_COLOR["red"]} Bad\n\n'
                                  f'{table}',
                             parse_mode='HTML')
    else:
        await message.answer(
            text=LEXICON_BOTH['error'])


@router.message(StateFilter(default_state))
async def echo(message: Message):
    """
    Fires if something unexpected is written to the chat
    """
    await message.reply(text=LEXICON_BOTH['error_enter'])
