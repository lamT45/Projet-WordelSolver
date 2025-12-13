# backend/app/routes/wordle.py
from fastapi import APIRouter
from app.services.wordle_solver import HybridWordleSolver

router = APIRouter()

# Charger dictionnaire FR + EN
with open("backend/app/services/words_fr.txt", encoding="utf-8") as f:
    words_fr = [w.strip().lower() for w in f.readlines() if len(w.strip())==5]

with open("backend/app/services/words_en.txt", encoding="utf-8") as f:
    words_en = [w.strip().lower() for w in f.readlines() if len(w.strip())==5]

# Ici on peut choisir français ou anglais
solver = HybridWordleSolver(word_list=words_fr + words_en)

@router.post("/guess")
def make_guess(feedback: dict):
    """
    feedback = {
        'green': {0:'a'},
        'yellow': {1:['b']},
        'grey': ['c','d']
    }
    """
    solver.update_constraints(feedback)
    next_guess = solver.get_next_guess()
    return {"next_guess": next_guess}
