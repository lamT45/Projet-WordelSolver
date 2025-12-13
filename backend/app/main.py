# backend/app/main.py
from fastapi import FastAPI
from app.routes import wordle

app = FastAPI(title="Wordle Solver API")

app.include_router(wordle.router, prefix="/wordle")
