import os
import asyncio
from litellm import acompletion
import litellm

# custom_pricing = {
#     "openrouter/anthropic/claude-3.5-haiku": {
#         "max_tokens": 8192,
#         "max_input_tokens": 200000,
#         "max_output_tokens": 8192,
#         "input_cost_per_token": 1e-06,
#         "output_cost_per_token": 5e-06,
#         "cache_creation_input_token_cost": 1.25e-06,
#         "cache_read_input_token_cost": 1e-07,
#         "search_context_cost_per_query": {
#             "search_context_size_low": 0.01,
#             "search_context_size_medium": 0.01,
#             "search_context_size_high": 0.01
#         },
#         "litellm_provider": "openrouter",
#         "mode": "chat",
#         "supports_function_calling": True,
#         "supports_vision": True,
#         "tool_use_system_prompt_tokens": 264,
#         "supports_assistant_prefill": True,
#         "supports_pdf_input": True,
#         "supports_prompt_caching": True,
#         "supports_response_schema": True,
#         "deprecation_date": "2025-10-01",
#         "supports_tool_choice": True,
#         "supports_web_search": True
#     }
# }

# # Pass custom_pricing to LiteLLM
# litellm.set_model_cost_map(custom_pricing)

os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENROUTER_API_BASE"] = "https://openrouter.ai/api/v1"
litellm._turn_on_debug()

os.environ["OR_SITE_URL"] = "" # [OPTIONAL]
os.environ["OR_APP_NAME"] = "" # [OPTIONAL]

# Reduced the text size to avoid network issues
huge_text = """
The Roman Empire was one of the most influential civilizations in history, ruling the Mediterranean basin and much of Europe at its height. Rome evolved from a monarchy to a republic in 509 BC, and then to an empire in 27 BC under Augustus.

Key features include:
- Political Structure: Centralized authority under emperors
- Territorial Extent: At its peak, covered 5 million square kilometers
- Military Power: Strong Roman army for conquest and control
- Cultural Influence: Contributions to law, engineering, and governance
- Decline: Western Empire fell in AD 476, Eastern in 1453

The story includes legends like Romulus and Remus, twin brothers raised by a wolf.
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

async def main():
    try:
        response = await acompletion(
            model="openrouter/anthropic/claude-3-5-haiku-20241022",  # or "openrouter/anthropic/claude-3-opus-20240229"
            messages=messages,
            stream=True,
            metadata={"hold_id": "afsdadascas"},
        )
        async for chunk in response:
            print(chunk)
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())