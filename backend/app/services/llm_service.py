import openai

# Mettre votre clé API dans backend/app/config.py
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def suggest_word(feedback):
    """
    Appel LLM OpenAI pour proposer le prochain mot.
    """
    prompt = f"""
    Voici le feedback du mot précédent:
    {feedback}
    Propose un mot anglais de 5 lettres qui maximise les chances de trouver le mot Wordle.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10
    )

    return response.choices[0].message.content.strip()
