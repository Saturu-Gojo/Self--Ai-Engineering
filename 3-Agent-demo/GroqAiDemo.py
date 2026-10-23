from dotenv import find_dotenv
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv(find_dotenv())

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

response = client.chat.completions.create(
    model = "qwen/qwen3.8-27b",
    messages=[
        {"role":"user","content":"What is Apple's stock ticker and current price?"}

    ]
)
print(response.choices)