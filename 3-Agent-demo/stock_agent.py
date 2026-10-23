import json
import os
from dotenv import load_dotenv
from groq import Groq
from yahoo_finance_demo import get_stock_price

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TOOL_DEFINITION = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get the current price of a stock given its ticker symbol",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker_symbol": {
                        "type": "string",
                        "description": "The ticker symbol of the stock to get the price e.g. AAPL, TSLA etc"
                    }
                },
                "required": ["ticker_symbol"]
            }
        }
    }
]

SYSTEM_PROMPT = """
You are a helpful stock market assistant. When the user asks about a stock price,
think step by step about what you need to do, then call the get_stock_price tool with
the correct ticker symbol. After receiving the result, present the information in a clear
and friendly manner.

IMPOERTANT: Always call the get_stock_price tool with the correct ticker symbol. Don't pick up
the price from our old conversation, as the price keep changeing. Don not assume
the price from previous conversation s. Always wnever a price for a stock is asked,
we need 

Always reason out loud so the user can follow your chain of thought.
"""

FEW_SHOT_EXAMPLES = [
    # Example 1: Single stock lookup
    {
        "role": "user",
        "content": "How much is Apple stock right now?"
    },
    {
        "role": "assistant",
        "content": (
            "The user is asking about Apple's stock price. Apple's ticker symbol is AAPL."
            "Let me fetch the current price of Apple stock."
        ),
        "tool_calls": [
            {
                "id": "tool_call_01",
                "type": "function",
                "function": {
                    "name": "get_stock_price",
                    "arguments": json.dumps({"ticker_symbol": "AAPL"})
                }
            }
        ]
    },
    {
        "role": "tool",
        "tool_call_id": "tool_call_01",
        "content": json.dumps({"ticker": "AAPL", "price": 200.30, "currency": "USD"}),
    },
    {
        "role": "assistant",
        "content": (
            "Apple (AAPL) is currently trading at $200.30 per share in USD."
            "Keep in mind this is the last traded price and may shift slightly by the time you check again."
        )
    },
    # Example 2: Multi stock comparison
    {
        "role": "user",
        "content": "Compare the stock prices of Google and Microsoft"
    },
    {
        "role": "assistant",
        "content": (
            "The user wants to compare two stocks. Google's parent company "
            "Alphabet trades under the ticker symbol GOOGL, and Microsoft trades "
            "under the ticker symbol MSFT."
            "Let me fetch the current prices of both stocks."
        ),
        "tool_calls": [
            {
                "id": "tool_call_02",
                "type": "function",
                "function": {
                    "name": "get_stock_price",
                    "arguments": json.dumps({"ticker_symbol": "GOOGL"})
                }
            },
            {
                "id": "tool_call_03",
                "type": "function",
                "function": {
                    "name": "get_stock_price",
                    "arguments": json.dumps({"ticker_symbol": "MSFT"})
                }
            }
        ]
    },
    {
        "role": "tool",
        "tool_call_id": "tool_call_02",
        "content": json.dumps({"ticker": "GOOGL", "price": 280.12, "currency": "USD"}),
    },
    {
        "role": "tool",
        "tool_call_id": "tool_call_03",
        "content": json.dumps({"ticker": "MSFT", "price": 235.77, "currency": "USD"}),
    },
    {
        "role": "assistant",
        "content": (
            "Here's the comparison:\n\n"
            "- Alphabet/Google (GOOGL) is trading at $280.12 per share in USD.\n"
            "- Microsoft (MSFT) is trading at $235.77 per share in USD.\n\n"
            "Microsoft's stock is currently cheaper than Google's."
        )
    }
]

# Map tool names to actual Python functions
AVAILABLE_TOOLS = {
    "get_stock_price": get_stock_price
}

def run_agent(query: str) -> None:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *FEW_SHOT_EXAMPLES,
        {"role": "user", "content": query},
    ]
    print("=" * 60)
    print(f"User: {query}")
    print("=" * 60)

    while True:
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",  # Or qwen/qwen-2.5-32b
            messages=messages,
            tools=TOOL_DEFINITION,
        )
        choice = response.choices[0]
        assistant_msg = choice.message

        messages.append(assistant_msg)

        if assistant_msg.content:
            print(f"Assistant: {assistant_msg.content}\n")

        # 1. If the model wants to call tools, execute them and continue the loop
        if assistant_msg.tool_calls:
            for tool_call in assistant_msg.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)

                print(f" [Tool call] {fn_name}({fn_args})")

                fn = AVAILABLE_TOOLS.get(fn_name)
                if not fn:
                    result = {"error": f"Tool {fn_name} not found"}
                else:
                    try:
                        result = fn(**fn_args)
                    except Exception as e:
                        result = {"error": str(e)}

                print(f" [Tool Result] {result}\n")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result) if not isinstance(result, str) else result,
                })
            # Continue loop so the model reads the tool output
            continue

        # 2. If no tool calls were requested, we are done
        break
    

def main():
    print("Stock price agent")
    print("-"*45)
    while True:
        query = input("\n You: ").strip()
        if not query:
            continue
        if query.lower() in ("quit","exit","q"):
            print("Good bye")
            break
        run_agent(query)

if __name__ == "__main__":
    main()