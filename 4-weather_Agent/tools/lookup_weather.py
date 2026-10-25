from config import FORECAST_URL
from config import WEATHER_REQUEST_TIMEOUT
from config import GECODE_URL
import requests

WEATHER_CODES: dict[int, str] = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    80: "rain showers",
    95: "thunderstorm",
    96: "thunderstorm with hail",
}

def lookup_weather(location:str)->str:

    try:

        geo = requests.get(
            GECODE_URL,
            params={"name":location,"count":1},
            timeout=WEATHER_REQUEST_TIMEOUT
        )

        geo.raise_for_status()
        matches = geo.json().get("results")

        if not matches:
            return f"we can't find matches"
        place = matches[0]
        lat, lon = place["latitude"], place["longitude"]

        label = ", ".join(
            p for p in (place.get("name"), place.get("country")) if p is not None
        )

        forecast = requests.get(
            FORECAST_URL,
            params={"latitude":lat, "longitude":lon, "current":"temperature_2m,weather_code,wind_speed_10m"},
            timeout=WEATHER_REQUEST_TIMEOUT,
        )

        forecast.raise_for_status()

        current= forecast.json().get("current")
        temperature = current.get("temperature_2m")
        weather_code = current.get("weather_code")
        wind_speed = current.get("wind_speed_10m")
        
        sky = WEATHER_CODES.get(weather_code,f"weather code is {weather_code}")
        wind_note = f" ,wind {wind_speed} km/hr" if wind_speed else ""

        return f"The current temperature is {temperature} C, the sky is {sky}{wind_note}."
    except requests.exceptions.RequestException as e:
        return f"We couldn't look up weather for {location}: {e}"
    except Exception as e:
         return f"We couldn't look up weather for {location} due some other issue: {e}"

print(lookup_weather("Lucknow"))