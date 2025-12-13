# backend/app/models/schemas.py
from typing import Dict, List
from pydantic import BaseModel, Field

class Feedback(BaseModel):
    """
    Schéma représentant le feedback d'une proposition Wordle.
    """
    green: Dict[int, str] = Field(
        default_factory=dict,
        description="Positions correctes avec la bonne lettre. Exemple: {0: 'a', 2: 'e'}"
    )
    yellow: Dict[int, List[str]] = Field(
        default_factory=dict,
        description="Lettres correctes mais à mauvaise position. Exemple: {1: ['a', 'e'], 3: ['r']}"
    )
    grey: List[str] = Field(
        default_factory=list,
        description="Lettres absentes dans le mot."
    )
