from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import wordle, llm
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wordle.router, prefix="/wordle", tags=["Wordle"])
app.include_router(llm.router, prefix="/llm", tags=["LLM"])

@app.get("/")
def root():
    return {"message": "Wordle Solver API is running"}
