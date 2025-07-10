import os
import asyncio
from litellm import acompletion
import litellm

litellm._turn_on_debug()

huge_text = """
messages = [The **Roman Empire** was one of the most influential and expansive civilizations in world history, ruling the Mediterranean basin, much of Europe, Western Asia, and North Africa at its height[1][4]. Its origins trace back to the city of Rome, traditionally founded in 753 BC along the River Tiber[2][4]. Rome evolved from a monarchy to a republic in 509 BC, and then to an empire in 27 BC when Augustus became the first emperor after a period of civil wars[1][2][3].
"""

messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are a historian studying the fall of the Roman Empire. You know the following book very well:"
            },
            {
                "type": "text",
                "text": huge_text,  # Replace with your large text
                "cache_control": {
                    "type": "ephemeral"
                }
            }
        ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Given the book below:"
        },
        {
          "type": "text",
          "text": huge_text,
          "cache_control": {
            "type": "ephemeral"
          }
        },
        {
          "type": "text",
          "text": "Name all the characters in the above book"
        }
      ]
    }
]

def wrap_text_with_cache_control(text):
    return [{"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}]


def add_cache_control(messages):
    """
    Add cache control to user and system messages.
    Supports both Bedrock and OpenRouter-style structured messages.
    Ensures cache_control is only added if not already present.
    """

    # Handle last user message (starting from the end)
    for i in range(len(messages) - 1, -1, -1):
        if messages[i].get("role") == "user":
            content = messages[i].get("content")

            if isinstance(content, list):
                last_part = content[-1]
                if "cache_control" not in last_part:
                    messages[i]["content"][-1]["cache_control"] = {"type": "ephemeral"}

            elif isinstance(content, str):
                messages[i]["content"] = wrap_text_with_cache_control(content)

            break  # Only modify the last user message

    # Handle all system messages
    for message in messages:
        if message.get("role") == "system":
            content = message.get("content")

            if isinstance(content, list):
                last_part = content[-1]
                if "cache_control" not in last_part:
                    message["content"][-1]["cache_control"] = {"type": "ephemeral"}

            elif isinstance(content, str):
                message["content"] = wrap_text_with_cache_control(content)

    return messages


def transform_body(body):
    """
    Transform the request body to add cache control and apply middleware transformations.
    This function is optimized for performance.
    """
    messages = body.get("messages", [])

    # Early return if no messages
    if not messages:
        return body

    # Apply cache control for Anthropic and OpenAI models
    model = body.get("model", "")
    if model.startswith("anthropic/"):
        messages = add_cache_control(messages)

    body["messages"] = messages

    return body


async def main():
    response = await acompletion(
        model="anthropic.claude-3-7-sonnet-20250219-v1:0",
        model_id="us.anthropic.claude-3-7-sonnet-20250219-v1:0",  # or "openrouter/anthropic/claude-3-opus-20240229"
        messages=messages,
        stream=True,
        aws_region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        metadata={"hold_id": "afsdadascas"},
    )
    async for chunk in response:
        print(chunk)

asyncio.run(main())
