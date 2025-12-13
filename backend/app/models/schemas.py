from pydantic import BaseModel
from typing import List

class LetterFeedback(BaseModel):
    letter: str
    status: str  # "green", "yellow", "gray"

class WordleRequest(BaseModel):
    guesses: List[List[LetterFeedback]]

class WordleResponse(BaseModel):
    suggestions: List[str]


