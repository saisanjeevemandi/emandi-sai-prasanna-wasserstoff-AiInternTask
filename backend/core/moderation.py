# backend/core/moderation.py

# Simple list-based profanity filter
BANNED_WORDS = {
    "damn", "hell", "shit", "fuck", "bastard", "idiot", "dumb"
    # Add more offensive terms as needed
}

def contains_profanity(text: str) -> bool:
    words = text.lower().split()
    return any(word in BANNED_WORDS for word in words)
