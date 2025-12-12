from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.wordle import router as wordle_router
from app.routes.llm import router as llm_router

app = FastAPI(
    title="Wordle Solver API",
    description="API backend pour le solveur Wordle utilisant CSP + LLM",
    version="1.0.0"
)

# CORS pour permettre au frontend React d'appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # à restreindre plus tard si besoin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⬇️ Inclusion des routes
app.include_router(wordle_router, prefix="/wordle", tags=["Wordle Solver"])
app.include_router(llm_router, prefix="/llm", tags=["LLM Integration"])


@app.get("/", summary="Health check")
async def root():
    return {"message": "Wordle Solver API is running!"}
