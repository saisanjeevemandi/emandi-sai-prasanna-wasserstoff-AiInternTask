# backend/core/rule_check.py

def does_beat(guess: str, seed: str) -> bool:
    guess = guess.lower()
    seed = seed.lower()

    winning_combos = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    return winning_combos.get(guess) == seed
