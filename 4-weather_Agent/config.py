from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

GECODE_URL = os.getenv("GECODE_URL", "https://geocoding-api.open-meteo.com/v1/search")

FORECAST_URL = os.getenv("FORECAST_URL", "https://api.open-meteo.com/v1/forecast")

WEATHER_REQUEST_TIMEOUT = int(os.getenv("WEATHER_REQUEST_TIMEOUT","10"))

PROJECT_ROOT = Path(__file__).parent.resolve()
PROMPTS_DIR = PROJECT_ROOT / "prompts"

SYSTEM_PROMPT_TEMPLATE = PROMPTS_DIR / "system.jinja"
GREETING_PROMPT_TEMPLATE = PROMPTS_DIR / "greeting.jinja"
MAX_TURNS = int(os.getenv("MAX_TURNS", "10"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS","4000"))