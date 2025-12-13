# backend/app/services/wordle_solver.py
from app.services.csp_solver import CSPSolver, WordleConstraints
from app.services.llm_service import GeminiLLM
from typing import List, Dict

class HybridWordleSolver:
    """
    Solveur hybride Wordle : CSP + LLM (Gemini)
    """
    def __init__(self, word_list: List[str], api_key: str = None):
        self.word_list = word_list
        self.constraints = WordleConstraints()
        self.past_guesses: List[str] = []

        # Initialise le solveur CSP
        self.csp = CSPSolver(word_length=5)
        self.csp.set_valid_words(word_list)

        # Initialise le LLM
        self.llm = GeminiLLM(api_key=api_key)

    def update_constraints(self, feedback: Dict):
        """
        Met à jour les contraintes selon le feedback du dernier mot.
        feedback = {
            'green': {pos: char},
            'yellow': {pos: [chars]},
            'grey': [chars]
        }
        """
        self.constraints.green.update(feedback.get("green", {}))
        for pos, letters in feedback.get("yellow", {}).items():
            self.constraints.yellow[pos].update(letters)
        self.constraints.grey.update(feedback.get("grey", []))

    def constraints_dict(self) -> Dict:
        """
        Convertit les contraintes en dict pour le LLM
        """
        return {
            "green": self.constraints.green,
            "yellow": {k: list(v) for k, v in self.constraints.yellow.items()},
            "grey": list(self.constraints.grey),
            "min_letter_counts": self.constraints.min_letter_counts
        }

    def get_next_guess(self, language: str = "fr") -> str:
        """
        Retourne le prochain mot à deviner
        """
        candidates = self.csp.filter_candidates(self.constraints)
        if not candidates:
            return "Aucun mot possible"

        guess = self.llm.suggest_word(candidates, self.constraints_dict(), language=language)
        self.past_guesses.append(guess)
        return guess

    def play_round(self, feedback: Dict, language: str = "fr") -> str:
        """
        Met à jour les contraintes et retourne le prochain mot
        """
        self.update_constraints(feedback)
        return self.get_next_guess(language=language)
