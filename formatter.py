from api_service import Weather


def weather_format(weather: Weather) -> str:
    """Formats weather data in string"""
    return str((f"City: {weather.city}",
                f"Temperature: {weather.temperature}°C",
                f"Weather: {weather.weather_type.value}"))
