from dotenv import load_dotenv
import os

load_dotenv()

GECODE_URL = os.getenv("GECODE_URL", "https://geocoding-api.open-meteo.com/v1/search")

FORECAST_URL = os.getenv("FORECAST_URL", "https://api.open-meteo.com/v1/forecast")

WEATHER_REQUEST_TIMEOUT = int(os.getenv("WEATHER_REQUEST_TIMEOUT","10"))