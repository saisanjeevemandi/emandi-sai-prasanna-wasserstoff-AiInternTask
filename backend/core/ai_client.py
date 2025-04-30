import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MAX_RETRIES = 3

async def validate_guess(seed: str, guess: str, persona: str = "default") -> str:
    prompt = generate_prompt(seed, guess, persona)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 5
    }

    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip().upper()
        except httpx.HTTPStatusError as e:
            if e.response.status_code in [429, 500, 503]:
                await asyncio.sleep(2 ** attempt)
            else:
                raise
    return "NO"

def generate_prompt(seed: str, guess: str, persona: str) -> str:
    base = f"Does '{guess}' beat '{seed}'?"
    if persona == "cheery":
        return base + " Please answer YES or NO with excitement!"
    elif persona == "serious":
        return base + " Respond clearly with only YES or NO."
    return base + " Answer only YES or NO."












# # backend/core/ai_client.py

# import os
# import httpx
# import asyncio
# from dotenv import load_dotenv

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# MAX_RETRIES = 3

# async def validate_guess(seed: str, guess: str) -> str:
#     prompt = (
#     f"You are a game judge in 'What Beats What'. Only answer YES if the guess "
#     f"logically beats the seed word in games like Rock Paper Scissors or common logic. "
#     f"Does '{guess}' beat '{seed}'? Respond strictly with YES or NO."
# )

#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "model": "llama3-8b-8192",
#         "messages": [{"role": "user", "content": prompt}],
#         "temperature": 0.5,
#         "max_tokens": 5
#     }

#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.post(
#                 "https://api.groq.com/openai/v1/chat/completions",
#                 headers=headers,
#                 json=payload
#             )
#         response.raise_for_status()
#         data = response.json()
#         return data["choices"][0]["message"]["content"].strip().upper()
#     except Exception as e:
#         print(f"❌ GROQ API ERROR: {e}")
#         return "NO"  # Fail-safe default