from prompts import build_system_prompt
import json

from client import build_client
from config import MAX_TURNS, MAX_TOKENS
from schemas import TOOL_MENU
from tools import TOOL_FUNCTION


def run_agent_turns(messages: list, max_turns: int = MAX_TURNS) -> str:

    # Build working copy — do NOT mutate the caller's list
    working = [
        {"role": "system", "content": build_system_prompt()},
        *messages,
    ]

    client, model, _ = build_client()

    for turn in range(max_turns):
        response = client.chat.completions.create(
            model=model,
            messages=working,
            tools=TOOL_MENU,
            max_tokens=MAX_TOKENS,
        )

        message = response.choices[0].message

        # No tool calls → this is the final answer
        if not message.tool_calls or turn == max_turns - 1:
            return message.content or ""

        # Append assistant's tool-call message to working history
        working.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            # arguments comes as a JSON string from the API — don't re-encode
                            "arguments": call.function.arguments,
                        },
                    }
                    for call in message.tool_calls
                ],
            }
        )

        # Execute each tool and append result
        for call in message.tool_calls:
            name = call.function.name
            if name not in TOOL_FUNCTION:
                tool_result = f"Unknown tool: {name}"
            else:
                arguments = json.loads(call.function.arguments)
                func = TOOL_FUNCTION[name]
                tool_result = func(**arguments)

            working.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "name": name,
                    "content": str(tool_result),
                }
            )

    return "Stopped due to max turns being reached"