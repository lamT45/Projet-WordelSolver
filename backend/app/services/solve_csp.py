from typing import List, Dict
from app.services.utils import filter_words


def build_constraints(guesses: List[List[Dict]]) -> Dict:
    """
    Transforme les retours Wordle en contraintes exploitables
    """
    constraints = {
        "green": {},     # position -> letter
        "yellow": [],    # (letter, position)
        "gray": set()    # letters
    }

    for guess in guesses:
        for pos, feedback in enumerate(guess):
            letter = feedback["letter"].lower()
            status = feedback["status"]

            if status == "green":
                constraints["green"][pos] = letter

            elif status == "yellow":
                constraints["yellow"].append((letter, pos))

            elif status == "gray":
                constraints["gray"].add(letter)

    return constraints


def solve_csp(
    words: List[str],
    guesses: List[List[Dict]]
) -> List[str]:
    """
    Applique les contraintes CSP pour filtrer les mots possibles
    """
    constraints = build_constraints(guesses)
    possible_words = filter_words(words, constraints)
    return possible_words


