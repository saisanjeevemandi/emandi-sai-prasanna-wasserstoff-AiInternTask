# backend/core/cache.py

import os
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_cached_result(seed, guess):
    key = f"{seed}:{guess}"
    return redis_client.get(key)

def set_cached_result(seed, guess, value):
    key = f"{seed}:{guess}"
    redis_client.set(key, value, ex=3600)  # Cache for 1 hour
