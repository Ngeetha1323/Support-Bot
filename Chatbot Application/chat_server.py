from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

# ==== 🔐 API Key ====
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "crJ3S6ZZkKRI4wIsykWaPd0sL4RmHnVD")  # Replace this with a secure method in production

# ==== 🚀 FastAPI App ====
app = FastAPI()

# ==== 🌐 CORS Config ====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== 🤖 Chat Endpoint ====
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    if not prompt:
        return {"response": "(Error): No prompt provided."}

    try:
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistral-medium",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return {"response": reply.strip()}

    except requests.exceptions.RequestException as req_err:
        return {"response": f"(Network Error): {str(req_err)}"}
    except Exception as e:
        return {"response": f"(Error): {str(e)}"}
