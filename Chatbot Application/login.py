# chat_server.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

MISTRAL_API_KEY = "crJ3S6ZZkKRI4wIsykWaPd0sL4RmHnVD"  # 🔐 Replace with valid key

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    try:
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mistral-medium",
            "messages": [{"role": "user", "content": prompt}]
        }

        resp = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload)
        result = resp.json()
        reply = result["choices"][0]["message"]["content"]
        return {"response": reply.strip()}
    except Exception as e:
        return {"response": f"(Error): {e}"}
