import os, asyncio, json, litellm
from litellm import acompletion, completion_cost

# Any long text ≥1 024 tokens (Sonnet min) so the checkpoint sticks
huge_text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum"  # ← keep your big Roman-Empire excerpt here

# Minimal cache-checkpoint message using Anthropic's API schema
message1 = [
    {
        "role": "system",
        "content": [
            {"type": "text",
             "text": "You are a historian studying the fall of the Roman Empire."},
            {"type": "text",
             "text": huge_text,
             "cache_control": {"type": "ephemeral"}
            }   # <- checkpoint
        ]
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Name all the characters in the above book", "cache_control": {"type": "ephemeral"}}
            # Removed invalid cache_control dict from user message content
        ]
    }
]

message2 = [
    {
        "role": "system",
        "content": [
            {"type": "text",
             "text": "You are a historian studying the fall of the Roman Empire."},
            {"type": "text",
             "text": huge_text,
             "cache_control": {"type": "ephemeral"}
            }   # <- checkpoint
        ]
    },
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Name all the characters in the above book"},
            {"type": "text", "text": "acascascascacasc", "cache_control": {"type": "ephemeral"}}
        ]
    }
]

async def main():
    resp = await acompletion(
        model          = "anthropic.claude-3-7-sonnet-20250219-v1:0",
        model_id       = "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        messages       = message1,
        stream         = True,                 # ← need full JSON for usage
        aws_region_name= "us-east-1",
        aws_access_key_id     = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        metadata = {"test": "first-run"},
    )
    async for chunk in resp:
        print(chunk)
    await asyncio.sleep(2)                 # keep TTL < 5 min
    resp = await acompletion(
        model          = "anthropic.claude-3-7-sonnet-20250219-v1:0",
        model_id       = "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        messages       = message2,
        stream         = True,                 # ← need full JSON for usage

        aws_region_name= "us-east-1",
        aws_access_key_id     = os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        metadata = {"test": "second-run"},
    )
    async for chunk in resp:
        print(chunk)

litellm._turn_on_debug()   # prints the raw Bedrock JSON
asyncio.run(main())
