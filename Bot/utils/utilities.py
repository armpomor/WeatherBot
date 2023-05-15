import json
from datetime import datetime, timedelta
from urllib.request import urlopen

from config.air_gases import GASES


def get_ip_data() -> dict:
    """
    Determines by IP coordinates, timezone,
    locality name, postal code, provider
    """
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    return json.load(response)


def convers_time(time_str: str) -> str:
    """
    Let's convert the string time from
    12 hour format to 24 hour format
    """
    delta = timedelta(hours=12)

    if time_str.endswith("PM"):
        t = datetime.strptime(time_str[:5], '%H:%M') + delta
        return t.strftime('%H:%M')

    return time_str[:5]


def calculation_day_long(time_1: str, time_2: str) -> str:
    """
    Calculate the length of the day
    """
    time_1 = convers_time(time_1)
    time_2 = convers_time(time_2)
    t1 = datetime.strptime(time_1, '%H:%M')
    t2 = datetime.strptime(time_2, '%H:%M')
    seconds = (t2 - t1).seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f'{hours} hours {minutes} minutes'


def set_color_air(n: float, gas: str) -> str:
    """
        Возвращает цвет плашки.
        Принимает значение и название газа,
        которое является ключом в словаре GASES.
        """
    x = [p for p in GASES[gas] if n in p]

    return GASES[gas][x[0]]


if __name__ == '__main__':
    print(calculation_day_long('05:19 AM', '07:30 PM'))
