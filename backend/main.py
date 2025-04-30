# backend/main.py

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

from fastapi import Request
from backend.core.moderation import contains_profanity
from backend.core.cache import get_cached_result, set_cached_result
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.core.game_logic import GuessLinkedList
from backend.core.ai_client import validate_guess

# Load DB config from .env
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS guess_counter (
    word TEXT PRIMARY KEY,
    count INTEGER DEFAULT 1
)
""")
conn.commit()

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory game state
game = GuessLinkedList()

# Request schema
class GuessRequest(BaseModel):
    seed: str
    guess: str

@app.get("/")
async def root():
    return {"message": "Server is running!"}

@app.post("/guess")
async def guess_handler(request: GuessRequest, http_req: Request):
    persona = http_req.headers.get("X-Host-Persona", "default")
    seed_word = request.seed
    guessed_word = request.guess

    # ✅ Check for inappropriate input
    if contains_profanity(guessed_word):
        return {
            "result": "Rejected",
            "reason": "Inappropriate guess detected. Please keep it clean.",
            "score": game.score
        }

    # ✅ Check Redis cache first
    cached_result = get_cached_result(seed_word, guessed_word)
    if cached_result:
        ai_result = cached_result
    else:
        ai_result = await validate_guess(seed_word, guessed_word, persona)
        set_cached_result(seed_word, guessed_word, ai_result)

    if ai_result != "YES":
        return {
            "result": "Wrong Guess",
            "message": f"{guessed_word} does NOT beat {seed_word}!",
            "score": game.score
        }

    success = game.add_guess(guessed_word)
    if not success:
        return {
            "result": "Game Over",
            "reason": "Duplicate guess detected!",
            "your_history": game.get_history(),
            "score": game.score
        }

    # ✅ Update database counter
    cursor.execute("""
        INSERT INTO guess_counter (word, count)
        VALUES (%s, 1)
        ON CONFLICT (word)
        DO UPDATE SET count = guess_counter.count + 1
    """, (guessed_word,))
    conn.commit()

    # ✅ Fetch global count
    cursor.execute("SELECT count FROM guess_counter WHERE word = %s", (guessed_word,))
    global_count = cursor.fetchone()[0]

    # ✅ Final response
    return {
        "result": "Correct Guess",
        "current_score": game.score,
        "guess_history": game.get_history(),
        "global_count": global_count
    }

@app.post("/reset")
async def reset_game():
    global game
    game = GuessLinkedList()
    return {"message": "Game reset successful."}