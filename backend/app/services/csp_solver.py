# backend/app/services/csp_solver.py
from ortools.sat.python import cp_model
from typing import List, Dict, Set
from collections import defaultdict, Counter

class WordleConstraints:
    """Stocke les contraintes du jeu Wordle"""
    def __init__(self):
        self.green: Dict[int, str] = {}       # Lettre correcte à la bonne position
        self.yellow: Dict[int, Set[str]] = defaultdict(set)  # Lettres correctes mais mauvaise position
        self.grey: Set[str] = set()           # Lettres absentes
        self.min_letter_counts: Dict[str, int] = {}  # Occurrences minimales par lettre

    def update(self, guess: str, feedback: List[str]):
        """
        Met à jour les contraintes selon un mot deviné et le feedback.
        feedback: liste ["green","yellow","grey"]
        """
        letter_counts = Counter()
        for i, (letter, fb) in enumerate(zip(guess, feedback)):
            if fb == "green":
                self.green[i] = letter
                letter_counts[letter] += 1
            elif fb == "yellow":
                self.yellow[i].add(letter)
                letter_counts[letter] += 1
            elif fb == "grey":
                if letter not in letter_counts:
                    self.grey.add(letter)

        for letter, count in letter_counts.items():
            current_min = self.min_letter_counts.get(letter, 0)
            self.min_letter_counts[letter] = max(current_min, count)

class CSPSolver:
    """Solveur CSP Wordle avec OR-Tools"""
    def __init__(self, word_length: int = 5):
        self.word_length = word_length
        self.valid_words: List[str] = []
        self.letter_set: Set[str] = set()

    def set_valid_words(self, words: List[str]):
        """Définit la liste des mots valides"""
        self.valid_words = [w.lower() for w in words if len(w) == self.word_length]
        self.letter_set = set("".join(self.valid_words))

    def filter_candidates(self, constraints: WordleConstraints, max_solutions: int = 1000) -> List[str]:
        """Retourne la liste de mots qui respectent les contraintes"""
        candidates = []

        for word in self.valid_words:
            if self._check_word(word, constraints):
                candidates.append(word)
                if len(candidates) >= max_solutions:
                    break
        return candidates

    def _check_word(self, word: str, constraints: WordleConstraints) -> bool:
        # Vérifier les lettres vertes
        for pos, letter in constraints.green.items():
            if word[pos] != letter:
                return False

        # Vérifier les lettres jaunes
        for pos, letters in constraints.yellow.items():
            for letter in letters:
                if word[pos] == letter or letter not in word:
                    return False

        # Vérifier les lettres grises
        for letter in constraints.grey:
            if letter in word and letter not in constraints.green.values() and all(letter not in letters for letters in constraints.yellow.values()):
                return False

        # Vérifier occurrences minimales
        for letter, min_count in constraints.min_letter_counts.items():
            if word.count(letter) < min_count:
                return False

        return True
