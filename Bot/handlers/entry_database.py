"""
The module runs every day and writes
the weather data to the database
"""
import asyncio

from database.postgresessions import session_add_row
from handlers.state_settings_handlers import engine
from utils.parsing_data import get_weather


async def writing_row():
    """
    The function writes
    weather data in database
    """
    data = get_weather()

    session_add_row(data, engine)


async def infinite_task():
    """
    The function is triggered once a day
    """
    while True:
        await writing_row()
        await asyncio.sleep(86400)
