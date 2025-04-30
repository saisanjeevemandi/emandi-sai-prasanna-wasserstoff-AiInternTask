# backend/core/game_logic.py

class Node:
    def __init__(self, guess):
        self.guess = guess
        self.next = None

class GuessLinkedList:
    def __init__(self, max_guesses=20):
        self.head = None
        self.guesses_set = set()
        self.score = 0
        self.max_guesses = max_guesses

    def add_guess(self, guess):
        if guess in self.guesses_set:
            return False
        if self.score >= self.max_guesses:
            return False  # prevent overload

        new_node = Node(guess)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

        self.guesses_set.add(guess)
        self.score += 1
        return True  # Successfully added

    def get_history(self):
        # Traverse the linked list and collect guesses
        history = []
        current = self.head
        while current:
            history.append(current.guess)
            current = current.next
        return history
