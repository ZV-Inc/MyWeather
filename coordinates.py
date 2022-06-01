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
        config.CITY_NAME = get_city_name(location.raw["display_name"])
        print(f"Location: {location}\nLatitude: {location.latitude}, Longitude: {location.longitude}")
        return Coordinates(longitude=location.longitude, latitude=location.latitude)
    except AttributeError:
        raise CantGetCity


def get_city_name(location: dict) -> str:
    city_name, num = "", 0
    while location[num] != ',':
        city_name += str(location[num])
        num += 1
    return city_name


def _round_coordinates(coordinates: Coordinates) -> Coordinates:
    if not config.USE_ROUNDED_COORDINATES:
        return coordinates
    return Coordinates(*map(lambda x: round(x, 2), [coordinates.latitude, coordinates.longitude]))
