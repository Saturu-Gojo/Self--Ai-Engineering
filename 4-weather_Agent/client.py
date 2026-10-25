from dataclasses import dataclass
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
@dataclass
class Provider:
    name:str
    env_var:str
    is_free:bool
    base_url:str
    model:str

PROVIDER = [
    Provider(
        name="Groq",
        env_var="GROQ_API_KEY",
        is_free=True,
        base_url=None,
        model="qwen/qwen3.8-27b"
    )
]

def select_provider()->Provider:
    for p in PROVIDER:
        if os.getenv(p.env_var):
            return p

    raise RuntimeError(f"No Provider is found")

def build_client()->tuple[Groq,str,Provider]:
    provider=select_provider()
    api_key = os.getenv(provider.env_var)
    if provider.base_url is None:
        client = Groq(api_key=api_key)
    else:
        client = Groq(api_key=api_key, base_url=provider.base_url)

    return client, provider.model, provider