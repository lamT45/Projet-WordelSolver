from collections import Counter
from typing import List, Dict


WORD_LENGTH = 5


def load_dictionary(path: str) -> List[str]:
    """
    Charge un fichier texte contenant un mot par ligne
    """
    with open(path, "r", encoding="utf-8") as f:
        words = [
            w.strip().lower()
            for w in f.readlines()
            if len(w.strip()) == WORD_LENGTH and w.isalpha()
        ]
    return words


def filter_words(
    words: List[str],
    constraints: Dict
) -> List[str]:
    """
    Filtre les mots selon les contraintes Wordle
    constraints = {
        "green": {position: letter},
        "yellow": [(letter, position)],
        "gray": [letter]
    }
    """
    filtered = []

    for word in words:
        valid = True

        # GREEN constraints
        for pos, letter in constraints.get("green", {}).items():
            if word[pos] != letter:
                valid = False
                break

        if not valid:
            continue

        # YELLOW constraints
        for letter, pos in constraints.get("yellow", []):
            if letter not in word or word[pos] == letter:
                valid = False
                break

        if not valid:
            continue

        # GRAY constraints
        for letter in constraints.get("gray", []):
            if letter in word:
                valid = False
                break

        if valid:
            filtered.append(word)

    return filtered


def score_words(words: List[str]) -> List[str]:
    """
    Score les mots selon la fréquence des lettres
    """
    letter_freq = Counter("".join(words))

    def score(word):
        return sum(letter_freq[c] for c in set(word))

    return sorted(words, key=score, reverse=True)


