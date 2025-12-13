from fastapi import APIRouter
from backend.app.services import solve_csp

router = APIRouter()

@router.get("/status")
def status():
    return {"message": "Wordle CSP Solver API is running"}

@router.post("/solve")
def solve_wordle(feedback: dict):
    """
    feedback: dict avec
    {
        "guess": "apple",
        "result": ["green", "gray", "yellow", "gray", "gray"]
    }
    """
    words = solve_csp.filter_words(feedback)
    return {"possible_words": words}
