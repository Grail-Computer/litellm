import asyncio
from litellm import completion, completion_cost
import litellm 
import os 
litellm.set_verbose = True # 👈 SEE RAW REQUEST
os.environ["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENROUTER_API_BASE"] = "https://openrouter.ai/api/v1"

N = 212
response = completion(
        model = "openrouter/anthropic/claude-3.7-sonnet",
        messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an AI assistant tasked with analyzing legal documents.",
                },
                {
                    "type": "text",
                    "text": "Here is the full text of a complex legal agreement" * N,
                    "cache_control": {"type": "ephemeral"},
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type":"text",
                    "text":"what are the key terms and conditions in this agreement?",
                    "cache_control": {"type": "ephemeral"},
                }
            ]
        },
    ]
)
cost = completion_cost(completion_response=response)
print(response.usage)
print(cost)

usage = response.usage

# Extract token counts
prompt_tokens = usage.prompt_tokens or 0
completion_tokens = usage.completion_tokens or 0
cache_creation_input_tokens = getattr(usage, "cache_creation_input_tokens", 0) or 0
cache_read_input_tokens = getattr(usage, "cache_read_input_tokens", 0) or 0
# prompt_tokens -= cache_read_input_tokens

# Calculate prices
input_price = (prompt_tokens / 1000) * 0.003
output_price = (completion_tokens / 1000) * 0.015
cache_write_price = (cache_creation_input_tokens / 1000) * 0.00375
cache_read_price = (cache_read_input_tokens / 1000) * 0.0003

total_price = input_price + output_price + cache_write_price + cache_read_price

print("Usage:", usage)
print(f"Input tokens: {prompt_tokens} (${input_price:.6f})")
print(f"Output tokens: {completion_tokens} (${output_price:.6f})")
print(f"Cache write input tokens: {cache_creation_input_tokens} (${cache_write_price:.6f})")
print(f"Cache read input tokens: {cache_read_input_tokens} (${cache_read_price:.6f})")
print(f"Total price: ${total_price:.6f}")


response = completion(
            model          = "openrouter/anthropic/claude-3.7-sonnet",

        messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "You are an AI assistant tasked with analyzing legal documents.",
                },
                {
                    "type": "text",
                    "text": "Here is the full text of a complex legal agreement" * N,
                    "cache_control": {"type": "ephemeral"},
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type":"text",
                    "text":"what are the key terms and conditions in this agreement?",
                    "cache_control": {"type": "ephemeral"},
                }
            ]
        },
        {
            "content":[
                    {
                        "type":"text",
                        "text":"I notice that the prompt contains repeated placeholder text rather than an actual legal agreement."
                    }
                ],
            "role":"assistant"
        },
        {
            "role": "user",
            "content": [
                {
                    "type":"text",
                    "text":"what are the key terms and conditions in this agreement?",
                    "cache_control": {"type": "ephemeral"},
                }
            ]
        },
    ],
)
# response.usage.prompt_tokens=response.usage.prompt_tokens - response.usage.cache_read_input_tokens
cost = completion_cost(completion_response=response)
# Calculate price based on the usage object and Anthropic Claude 3.7 Sonnet pricing
# Pricing (per 1,000 tokens):
#   Input tokens: $0.003
#   Output tokens: $0.015
#   Cache write input tokens: $0.00375
#   Cache read input tokens: $0.0003

usage = response.usage

# Extract token counts
prompt_tokens = usage.prompt_tokens or 0
completion_tokens = usage.completion_tokens or 0
cache_creation_input_tokens = getattr(usage, "cache_creation_input_tokens", 0) or 0
cache_read_input_tokens = getattr(usage, "cache_read_input_tokens", 0) or 0
# prompt_tokens -= cache_read_input_tokens

# Calculate prices
input_price = (prompt_tokens / 1000) * 0.003
output_price = (completion_tokens / 1000) * 0.015
cache_write_price = (cache_creation_input_tokens / 1000) * 0.00375
cache_read_price = (cache_read_input_tokens / 1000) * 0.0003

total_price = input_price + output_price + cache_write_price + cache_read_price

print("Usage:", usage)
print(f"Input tokens: {prompt_tokens} (${input_price:.6f})")
print(f"Output tokens: {completion_tokens} (${output_price:.6f})")
print(f"Cache write input tokens: {cache_creation_input_tokens} (${cache_write_price:.6f})")
print(f"Cache read input tokens: {cache_read_input_tokens} (${cache_read_price:.6f})")
print(f"Total price: ${total_price:.6f}")
