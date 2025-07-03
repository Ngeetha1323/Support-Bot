import requests

class AIChatClient:
    def __init__(self, api_url="http://localhost:8000/chat"):
        self.api_url = api_url

    def get_response(self, user_prompt: str) -> str:
        full_prompt = f"Please respond in English only.\n\nUser: {user_prompt}"
        try:
            res = requests.post(self.api_url, json={"prompt": full_prompt})
            if res.status_code == 200:
                return res.json().get("response", "(No reply)")
            else:
                return f"(Error {res.status_code}) {res.text}"
        except Exception as e:
            return f"(Server error: {e})"

# === Terminal chat app ===
if __name__ == "__main__":
    print("🧠 AI Chat Client (Type 'exit' to quit)\n")
    bot = AIChatClient()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        reply = bot.get_response(user_input)
        print("AI:", reply)
