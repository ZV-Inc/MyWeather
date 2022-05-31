class CantGetCity(Exception):
    """Wrong city name or geopy service not available"""
    pass


class ApiServiceError(Exception):
    """OpenWeather API not available"""
    pass
