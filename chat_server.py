# chat_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

# ✅ FastAPI app
app = FastAPI()

# ✅ CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace * with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Fireworks API setup
FIREWORKS_API_KEY = "fw_3ZaLYVvP4F19As9hDxwEPgam"
MODEL_ID = "accounts/fireworks/models/qwen3-235b-a22b"
FIREWORKS_URL = "https://api.fireworks.ai/inference/v1/completions"

class PromptRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat(request: PromptRequest):
    headers = {
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_ID,
        "prompt": request.prompt,
        "max_tokens": 2048,
        "temperature": 0.7
    }

    try:
        response = requests.post(FIREWORKS_URL, headers=headers, json=payload)
        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            return {"response": data["choices"][0]["text"].strip()}
        else:
            return {"response": f"(No reply)\nFull API response: {data}"}

    except Exception as e:
        return {"response": f"(Server error): {e}"}
