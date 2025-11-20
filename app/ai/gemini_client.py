import os
from google import generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "models/gemini-2.0-flash"


def get_model():
    return genai.GenerativeModel(MODEL_NAME)

def run_json_prompt(prompt: str) -> dict:
    """
    Enforces strict JSON response.
    The caller must validate the output.
    """
    model = get_model()
    response = model.generate_content(
        prompt,
        generation_config={
            "response_mime_type": "application/json"
        }
    )
    return response.text
