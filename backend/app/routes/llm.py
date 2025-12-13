# backend/app/routes/llm.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.llm_service import LLMService
from app.models.schemas import Feedback, WordGuess

router = APIRouter(
    prefix="/llm",
    tags=["LLM"]
)

# Schéma pour la requête LLM
class LLMRequest(BaseModel):
    candidates: List[str]                   # Liste de mots candidats filtrés par CSP
    past_guesses: Optional[List[str]] = []  # Historique des propositions
    feedback_history: Optional[List[Feedback]] = []  # Feedbacks précédents
    word_length: int = 5                     # Taille du mot

# Schéma pour la réponse LLM
class LLMResponse(BaseModel):
    suggested_word: str
    explanation: str

# Initialisation du service LLM
llm_service = LLMService()

@router.post("/suggest", response_model=LLMResponse)
async def suggest_word(req: LLMRequest):
    """
    Endpoint LLM : propose le mot optimal à deviner parmi les candidats
    en utilisant l'historique et le feedback.
    """
    if not req.candidates:
        raise HTTPException(status_code=400, detail="La liste des candidats est vide")

    try:
        suggested_word, explanation = llm_service.suggest_word(
            candidates=req.candidates,
            past_guesses=req.past_guesses,
            feedback_history=req.feedback_history,
            word_length=req.word_length
        )
        return LLMResponse(suggested_word=suggested_word, explanation=explanation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur LLM : {str(e)}")
