USE_ROUNDED_COORDINATES = False
CITY = str
OPENWEATHER_API = "8ca35389848358398b8622beef50de65"
OPENWEATHER_URL = ("https://api.openweathermap.org/data/2.5/weather?"
                   "lat={latitude}&lon={longitude}"
                   f"&appid={OPENWEATHER_API}"
                   "&lang=en"
                   "&units=metric")
