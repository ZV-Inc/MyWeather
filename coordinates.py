from typing import NamedTuple
from geopy.geocoders import Nominatim
from exceptions import CantGetCity
import config


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_city_coordinates() -> Coordinates:
    """Returns city coordinates"""
    try:
        geolocator = Nominatim(user_agent="coordinates")
        user_answer = input("Enter city name to get weather: ")
        location = geolocator.geocode(user_answer)
        city_coordinates = _round_coordinates(Coordinates(longitude=location.longitude, latitude=location.latitude))
        config.CITY_NAME = _get_city_name(location.raw["display_name"])
        print(f"Location: {location} ",
              f"Latitude: {city_coordinates.latitude}, ",
              f"Longitude: {city_coordinates.longitude}")
        return Coordinates(longitude=city_coordinates.longitude, latitude=city_coordinates.latitude)
    except AttributeError:
        raise CantGetCity


def _get_city_name(location: dict) -> str:
    city_name, num = "", 0
    if not location.__contains__(","):
        return f"Unavailable to get city. Result: {location}"

    while location[num] != ',':
        city_name += str(location[num])
        num += 1
    return city_name


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDINATES:
        return coordinates
    return Coordinates(*map(lambda x: round(x, 2), [coordinates.latitude, coordinates.longitude]))
