#!/usr/bin/env python3.10
import config
from coordinates import get_city_coordinates
from api_service import get_weather
from formatter import weather_format
from exceptions import CantGetCity, ApiServiceError


def main():
    try:
        city_coordinates = get_city_coordinates()
    except CantGetCity:
        print("The city could not be found. "
              "Maybe you made a mistake in the name of the city "
              "or the OpenWeather service is not available.")
        exit(1)
    try:
        weather = get_weather(city_coordinates)
    except ApiServiceError:
        print(f"Unable to get weather data for your city ({config.CITY_NAME}).")
        exit(1)
    print(weather_format(weather))


if __name__ == "__main__":
    main()
