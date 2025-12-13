from fastapi import APIRouter
from app.services import llm_service

router = APIRouter()

@router.get("/status")
def status():
    return {"message": "LLM endpoint is running"}

@router.post("/suggest")
def suggest_word(feedback: dict):
    """
    feedback: dict comme pour /solve
    """
    suggestion = llm_service.suggest_word(feedback)
    return {"suggestion": suggestion}
