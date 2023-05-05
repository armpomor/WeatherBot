from aiogram.filters.state import State, StatesGroup


class FSMSettings(StatesGroup):
    """
    FSM settings
    """
    set_language = State()  # Enter language
    set_device = State()  # Enter device
    set_location = State()  # Enter location


class FSMForecast(StatesGroup):
    """
    FSM forecast
    """
    select_forecast = State()  # Select forecast
