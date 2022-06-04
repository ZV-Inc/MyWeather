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
    # Thunderstorm\Гроза
    THUNDERSTORM_WITH_LIGHT_RAIN = "Thunderstorm with light rain"
    THUNDERSTORM_WITH_RAIN = "Thunderstorm with rain"
    THUNDERSTORM_WITH_HEAVY_RAIN = "Thunderstorm with heavy rain"
    LIGHT_THUNDERSTORM = "Light thunderstorm"
    THUNDERSTORM = "Thunderstorm"
    HEAVY_THUNDERSTORM = "Heavy thunderstorm"
    RAGGED_THUNDERSTORM = "Ragged thunderstorm"
    THUNDERSTORM_WITH_LIGHT_DRIZZLE = "Thunderstorm with light drizzle"
    THUNDERSTORM_WITH_DRIZZLE = "Thunderstorm with drizzle"
    THUNDERSTORM_WITH_HEAVY_DRIZZLE = "Thunderstorm with heavy drizzle"

    # Drizzle\Изморось
    LIGHT_INTENSITY_DRIZZLE = "Light intensity drizzle"
    DRIZZLE = "Drizzle"
    HEAVY_INTENSITY_DRIZZLE = "Heavy intensity drizzle"
    LIGHT_INTENSITY_DRIZZLE_RAIN = "Light intensity drizzle rain"
    DRIZZLE_RAIN = "Drizzle rain"
    HEAVY_INTENSITY_DRIZZLE_RAIN = "Heavy intensity drizzle rain"
    SHOWER_RAIN_AND_DRIZZLE = "Shower rain and drizzle"
    HEAVY_SHOWER_RAIN_AND_DRIZZLE = "Heavy shower rain and drizzle"
    SHOWER_DRIZZLE = "Shower drizzle"

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

    # Snow\Снег
    LIGHT_SNOW = "Light snow"
    SNOW = "Snow"
    HEAVY_SNOW = "Heavy snow"
    SLEET = "Sleet"
    LIGHT_SHOWER_SLEET = "Light shower snow"
    SHOWER_SLEET = "Shower sleet"
    LIGHT_RAIN_AND_SNOW = "Light rain and snow"
    RAIN_AND_SNOW = "Rain and snow"
    LIGHT_SHOWER_SNOW = "Light shower snow"
    SHOWER_SNOW = "Shower snow"
    HEAVY_SHOWER_SNOW = "Heavy shower snow"

    # Atmosphere\Атмосфера
    MIST = "Mist"
    SMOKE = "Smoke"
    HAZE = "Haze"
    SAND_OR_DUST_WHIRS = "Sand or dust whirs"
    FOG = "Fog"
    SAND = "Sand"
    DUST = "Dust"
    VOLCANIC_ASH = "Volcanic ash"
    SQUALLS = "Squalls"
    TORNADO = "Tornado"

    # Clear\Ясно
    CLEAR = "Clear"   # "Ясно"

    # Clouds\Облачно
    FEW_CLOUDS = "Few clouds"   # "Малооблачно"
    SCATTERED_CLOUDS = "Scattered clouds"   # "Рассеянные облака"
    BROKEN_CLOUDS = "Broken clouds"   # "Рваные облака"
    OVERCAST_CLOUDS = "Overcast clouds"   # "Пасмурно"


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
                   city=str(config.CITY_NAME),
                   weather_type=_parse_weather_type(openweather_dict))


def _parse_temperature(openweather_dict: dict) -> temp_celsius:
    return round(openweather_dict["main"]["temp"])


def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict["weather"][0]["id"])
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_types = {
        # Thunderstorm\Гроза
        "200": WeatherType.THUNDERSTORM_WITH_LIGHT_RAIN,
        "201": WeatherType.THUNDERSTORM_WITH_RAIN,
        "202": WeatherType.THUNDERSTORM_WITH_HEAVY_RAIN,
        "210": WeatherType.LIGHT_THUNDERSTORM,
        "211": WeatherType.THUNDERSTORM,
        "212": WeatherType.HEAVY_THUNDERSTORM,
        "221": WeatherType.RAGGED_THUNDERSTORM,
        "230": WeatherType.THUNDERSTORM_WITH_LIGHT_DRIZZLE,
        "231": WeatherType.THUNDERSTORM_WITH_DRIZZLE,
        "232": WeatherType.THUNDERSTORM_WITH_HEAVY_DRIZZLE,

        # Drizzle\Изморось
        "300": WeatherType.LIGHT_INTENSITY_DRIZZLE,
        "301": WeatherType.DRIZZLE,
        "302": WeatherType.HEAVY_INTENSITY_DRIZZLE,
        "310": WeatherType.LIGHT_INTENSITY_DRIZZLE_RAIN,
        "311": WeatherType.DRIZZLE_RAIN,
        "312": WeatherType.HEAVY_INTENSITY_DRIZZLE_RAIN,
        "313": WeatherType.SHOWER_RAIN_AND_DRIZZLE,
        "314": WeatherType.HEAVY_SHOWER_RAIN_AND_DRIZZLE,
        "321": WeatherType.SHOWER_DRIZZLE,

        # Rain\Дождь
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

        # Snow\Снег
        "600": WeatherType.LIGHT_SNOW,
        "601": WeatherType.SNOW,
        "602": WeatherType.HEAVY_SNOW,
        "611": WeatherType.SLEET,
        "612": WeatherType.LIGHT_SHOWER_SLEET,
        "613": WeatherType.SHOWER_SLEET,
        "615": WeatherType.LIGHT_RAIN_AND_SNOW,
        "616": WeatherType.RAIN_AND_SNOW,
        "620": WeatherType.LIGHT_SHOWER_SNOW,
        "621": WeatherType.SHOWER_SNOW,
        "622": WeatherType.HEAVY_SHOWER_SNOW,

        # Atmosphere\Атмосфера
        "701": WeatherType.MIST,
        "711": WeatherType.SMOKE,
        "721": WeatherType.HAZE,
        "731": WeatherType.SAND_OR_DUST_WHIRS,
        "741": WeatherType.FOG,
        "751": WeatherType.SAND,
        "761": WeatherType.DUST,
        "762": WeatherType.VOLCANIC_ASH,
        "771": WeatherType.SQUALLS,
        "781": WeatherType.TORNADO,

        "800": WeatherType.CLEAR,

        "801": WeatherType.FEW_CLOUDS,
        "802": WeatherType.SCATTERED_CLOUDS,
        "803": WeatherType.BROKEN_CLOUDS,
        "804": WeatherType.OVERCAST_CLOUDS
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError
