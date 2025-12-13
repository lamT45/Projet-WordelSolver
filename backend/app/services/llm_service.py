# backend/app/services/llm_service.py
from typing import List
import os
import requests

class GeminiLLM:
    """
    Service d'intégration d'un LLM (ex: Gemini) pour suggérer des mots Wordle
    """
    def __init__(self, api_key: str = None, model: str = "gemini-1.5-mini"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model
        self.endpoint = "https://api.gemini.ai/v1/chat/completions"  # exemple

    def suggest_word(self, candidates: List[str], constraints: dict, language: str = "fr") -> str:
        """
        Retourne le mot suggéré par le LLM selon les contraintes
        candidates: liste des mots valides filtrés par CSP
        constraints: dict {"green": {}, "yellow": {}, "grey": [], "min_letter_counts": {}}
        language: "fr" ou "en"
        """
        # Construire le prompt
        prompt = f"""
Tu es un expert Wordle {language.upper()}.
Tu dois proposer le mot suivant à deviner.
Liste des candidats possibles: {', '.join(candidates[:50])}...
Contraintes:
- Vertes (position exacte): {constraints.get('green', {})}
- Jaunes (lettres présentes mais mauvaise position): {constraints.get('yellow', {})}
- Grises (lettres absentes): {constraints.get('grey', [])}
- Occurrences minimales: {constraints.get('min_letter_counts', {})}

Choisis le mot qui maximise les chances de trouver le mot cible. 
Répond uniquement par le mot, sans explication.
"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": f"Tu es un expert Wordle {language.upper()}."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 5
        }

        response = requests.post(self.endpoint, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Erreur LLM: {response.status_code} - {response.text}")

        try:
            data = response.json()
            # Extraction du mot depuis la réponse du LLM
            word = data['choices'][0]['message']['content'].strip().split()[0].lower()
            return word
        except Exception as e:
            raise Exception(f"Impossible d'extraire le mot du LLM: {e}")

