import requests

from config.config import API, COORDINATES, LANG, URL


# from config.config_dev import API, COORDINATES, LANG, URL


class Weather:
    """
    Weather request
    """

    def __init__(self, key=API, q=COORDINATES, lang=LANG, url=URL, days=None, dt=None, hour=None, end_dt=None):
        self.key: str = key  # API key
        self.q: str = q  # Coordinates or IP address or city name.
        self.lang: str = lang
        self.url: str = url
        self.days: int = days  # How many days is the forecast. 1 to 14
        self.dt: str = dt  # Forecast or history for a specific day. Format yyyy-MM-dd
        self.hour: int = hour  # From 1 to 24. If passed, then the forecast or history for this hour
        self.end_dt: str = end_dt  # If passed, then forecast or history up to that date. Format yyyy-MM-dd

    def real_time(self) -> dict:
        """
        Current weather
        """
        current_weather = requests.get(f'{self.url}/current.json',
                                       params={'key': self.key, 'q': self.q, 'lang': self.lang, 'aqi': 'yes'})
        return current_weather.json()

    def get_forecast(self) -> dict:
        """
        Returns forecast for days days. With days=None forecast
        for the current day. If hour is passed, then forecast for
        a certain hour, and if not transmitted, then the forecast for
        each hour. If dt - then the forecast for a specific day.
        """
        forecast_weather = requests.get(f'{self.url}/forecast.json',
                                        params={'key': self.key, 'q': self.q, 'lang': self.lang, 'days': self.days})
        return forecast_weather.json()

    def get_astronomy(self) -> dict:
        """
        Returns the phases of the moon, sunrise and sunset times.
        If the date dt is passed, then on that date.
        """
        astronomy = requests.get(f'{self.url}/astronomy.json',
                                 params={'key': self.key, 'q': self.q, 'lang': self.lang})
        return astronomy.json()


if __name__ == '__main__':
    weather = Weather(days=3)
    real_weather = weather.real_time()
    forecast = weather.get_forecast()
    astronomy = weather.get_astronomy()
