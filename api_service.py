import json
import ssl
import config
import urllib.request
from typing import NamedTuple
from enum import Enum
from urllib.error import URLError
from coordinates import Coordinates
from json.decoder import JSONDecodeError
from exceptions import ApiServiceError

temp_celsius = float


class WeatherType(Enum):
    # Rain\Дождь
    LIGHT_RAIN = "Light rain"                                       # "Лёгкий дождь"
    MODERATE_RAIN = "Moderate rain"                                 # "Умеренный дождь"
    HEAVY_INTENSITY_RAIN = "Heavy intensity rain"                   # "Сильный интенсивный дождь"
    VERY_HEAVY_RAIN = "Very heavy rain"                             # "Очень сильный дождь"
    EXTREME_RAIN = "Extreme"                                        # "Град"
    FREEZING_RAIN = "Freezing rain"                                 # "Дождь со снегом"
    LIGHT_INTENSITY_SHOWER_RAIN = "Light intensity shower rain"     # "Слабый ливень"
    SHOWER_RAIN = "Shower rain"                                     # "Ливень"
    HEAVY_INTENSITY_SHOWER_RAIN = "Heavy intensity shower rain"     # "Сильный ливень"
    RAGGED_SHOWER_RAIN = "Ragged shower rain"                       # "Прерывистый ливень"

    # Clouds\Облачно
    CLOUDS = "Clouds"   # "Облачно"

    # Snow\Снег
    SNOW = "Snow"   # "Снег"

    # Thunder\Гроза
    THUNDER = "Thunder"   # "Гроза"

    # Fog\Туман
    FOG = "Fog"   # "Туман"

    # Clear\Ясно
    CLEAR = "Clear"   # "Ясно"


class Weather(NamedTuple):
    temperature: temp_celsius
    city: str
    weather_type: WeatherType


def get_weather(coordinates: Coordinates) -> Weather:
    """Weather from OpenWeather"""
    openweather_response = _get_openweather_response(
        longitude=coordinates.longitude, latitude=coordinates.latitude)
    weather = _parse_openweather_response(openweather_response)
    return weather


def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URL.format(latitude=latitude, longitude=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(temperature=_parse_temperature(openweather_dict),
                   city=str(config.CITY),
                   weather_type=_parse_weather_type(openweather_dict))


def _parse_temperature(openweather_dict: dict) -> temp_celsius:
    return round(openweather_dict["main"]["temp"])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict["weather"][0]["id"])
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_types = {
        "1": WeatherType.THUNDER,
        "500": WeatherType.LIGHT_RAIN,
        "501": WeatherType.MODERATE_RAIN,
        "502": WeatherType.HEAVY_INTENSITY_RAIN,
        "503": WeatherType.VERY_HEAVY_RAIN,
        "504": WeatherType.EXTREME_RAIN,
        "511": WeatherType.FREEZING_RAIN,
        "520": WeatherType.LIGHT_INTENSITY_SHOWER_RAIN,
        "521": WeatherType.SHOWER_RAIN,
        "522": WeatherType.HEAVY_INTENSITY_SHOWER_RAIN,
        "531": WeatherType.RAGGED_SHOWER_RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError
