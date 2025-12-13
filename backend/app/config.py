from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME = "Wordle Solver API"

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    ALLOWED_ORIGINS = [
        "http://localhost:5173",  # frontend Vite
        "http://localhost:3000"   # frontend CRA
    ]

settings = Settings()
