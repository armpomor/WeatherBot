import time

from config.config import COORDINATES, LANG
# from config.config_dev import COORDINATES, LANG
from config.your_location import LOCALE  # Create a file with your coordinates
from utils.utilities import convers_time, calculation_day_long
from utils.weather import Weather


def parse_real_time(coordinates=COORDINATES, lang=LANG) -> dict:
    """
    Extract temp, condition, wind_dir,
    wind_kph, icon, humidity, cloud.
    weather['current']['temp_c'] = float
    weather['current']['condition']['text'] = str
    weather['current']['wind_kph'] = float  kph/3.6 = m/s
    weather['current']['wind_dir'] = str
    weather['current']['humidity'] = int  %
    weather['current']['pressure_mb'] = int millibars/1.333 = мм рт. ст.
    weather['current']['precip_mm'] = int  mm
    weather['current']['cloud'] = int  %
    weather['current']['condition']['code'] = int Weather condition unique code.
    """
    weather = Weather(q=coordinates, lang=lang).real_time()

    key = ['temp', 'condition', 'wind_mps', 'wind_dir', 'humidity', 'pressure_mb', 'precip_mm', 'cloud', 'code']
    value = [weather['current']['temp_c'], weather['current']['condition']['text'],
             round(weather['current']['wind_kph'] / 3.6, 1), weather['current']['wind_dir'],
             weather['current']['humidity'], int(weather['current']['pressure_mb'] / 1.333),
             weather['current']['precip_mm'],
             weather['current']['cloud'], weather['current']['condition']['code']]

    result = dict(zip(key, value))

    return result


def parse_forecast(coordinates=COORDINATES, lang=LANG) -> list[dict]:
    """
    Forecast 3 days.
    Extract date, maxtemp_c, mintemp_c, maxwind_kph,
    avghumidity, condition, icon.
    ['date'] - str
    ['day']['maxtemp_c'] - float
    ['day']['mintemp_c'] - float
    ['day']['maxwind_kph'] - float
    ['day']['avghumidity'] - int
    ['day']['totalprecip_mm'] - float
    ['day']['condition']['text'] - str
    ['day']['condition']['code'] - int Weather condition unique code.
    """
    weather = Weather(q=coordinates, days=3, lang=lang).get_forecast()

    weather_days = []

    for i in weather['forecast']['forecastday']:
        date = dict()

        date['date_time'] = i['date']
        date['maxtemp_c'] = i['day']['maxtemp_c']
        date['mintemp_c'] = i['day']['mintemp_c']
        date['maxwind_kph'] = round(i['day']['maxwind_kph'] / 3.6, 1)
        date['avghumidity'] = i['day']['avghumidity']
        date['totalprecip_mm'] = i['day']['totalprecip_mm']
        date['condition'] = i['day']['condition']['text']
        date['code'] = i['day']['condition']['code']

        weather_days.append(date)

    return weather_days


def parse_astro(coordinates=COORDINATES) -> dict:
    """
    Extract sunrise, sunset.
    Return:
        sunrise - str
        sunset - str
        long_day - str
    """
    weather = Weather(q=coordinates, days=1).get_forecast()

    sunrise = weather['forecast']['forecastday'][0]['astro']['sunrise']
    sunset = weather['forecast']['forecastday'][0]['astro']['sunset']
    long_day = calculation_day_long(time_1=sunrise, time_2=sunset)
    sunrise = convers_time(sunrise)
    sunset = convers_time(sunset)

    astro = dict()

    astro['sunrise'] = sunrise
    astro['sunset'] = sunset
    astro['long_day'] = long_day

    return astro


def parse_air_quality(coordinates=COORDINATES) -> dict:
    """
    Extract co - float, no2 - float,
    o3 - float, so2 - float, pm2_5 - float,
    pm10 - float.
    """
    weather = Weather(q=coordinates).real_time()

    air = dict()

    air['CO'] = round(weather['current']['air_quality']['co'], 2)
    air['NO2'] = round(weather['current']['air_quality']['no2'], 2)
    air['O3'] = round(weather['current']['air_quality']['o3'], 2)
    air['SO2'] = round(weather['current']['air_quality']['so2'], 2)
    air['pm2_5'] = round(weather['current']['air_quality']['pm2_5'], 2)
    air['pm10'] = round(weather['current']['air_quality']['pm10'], 2)

    return air


def get_weather() -> dict:
    """
    The function runs parsers and builds a dictionary
    from the data to be written to the weather table in the database.
    LOCALE - these are your coordinates.
    """
    data = dict()

    today = parse_forecast(LOCALE, LANG)[0]
    time.sleep(5)

    astro = parse_astro(LOCALE)
    time.sleep(5)

    air = parse_air_quality(LOCALE)
    time.sleep(5)

    time_real = parse_real_time(LOCALE, LANG)

    data['date_time'] = today['date_time']
    data['temp_max'] = today['maxtemp_c']
    data['temp_min'] = today['mintemp_c']
    data['wind_mps'] = today['maxwind_kph']
    data['humidity'] = today['avghumidity']
    data['precipitation'] = today['totalprecip_mm']
    data['condition'] = today['condition']
    data['sunrise'] = astro['sunrise']
    data['sunset'] = astro['sunset']
    data['long_day'] = astro['long_day']
    data['cloud'] = time_real['cloud']
    data['pressure'] = time_real['pressure_mb']
    data['air_co'] = air['CO']
    data['air_no2'] = air['NO2']
    data['air_o3'] = air['O3']
    data['air_so2'] = air['SO2']
    data['air_pm2_5'] = air['pm2_5']
    data['air_pm10'] = air['pm10']

    return data


if __name__ == '__main__':
    # for key, value in parse_real_time().items():
    #     print(key, ':', value)

    for key, value in parse_air_quality('69.408, 30.207').items():
        print(key, ':', value)


