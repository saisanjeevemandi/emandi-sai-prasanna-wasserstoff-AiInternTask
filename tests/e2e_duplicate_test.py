# tests/e2e_duplicate_test.py

import requests

BASE_URL = "http://localhost:8000"

def test_duplicate_guess_flow():
    seed = "Rock"
    guess = "Paper"

    # First correct guess
    response = requests.post(f"{BASE_URL}/guess", json={"seed": seed, "guess": guess})
    assert response.status_code == 200
    assert response.json()["result"] == "Correct Guess"

    # Second duplicate guess → should end the game
    response = requests.post(f"{BASE_URL}/guess", json={"seed": seed, "guess": guess})
    assert response.status_code == 200
    assert response.json()["result"] == "Game Over"
