import requests

def get_ai_response(prompt: str) -> str:
    API_URL = "http://localhost:8000/chat"  # Make sure your FastAPI server runs here

    try:
        response = requests.post(API_URL, json={"prompt": prompt})
        if response.status_code == 200:
            return response.json().get("response", "(No reply)")
        else:
            return f"(Error {response.status_code}) {response.text}"
    except Exception as e:
        return f"(Server error: {e})"

# === Test it ===
if __name__ == "__main__":  # ✅ FIXED this line
    user_prompt = input("You: ")
    ai_reply = get_ai_response(user_prompt)
    print("AI:", ai_reply)

