import os
import json
import datetime

# === CONFIG ===
USER_DB = "users.json"
CHAT_HISTORY_DIR = "chats"
API_URL = "http://localhost:8000/chat"

# === CSS STYLE ===
CHATBOT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');

.stApp {
    background: linear-gradient(135deg, #050505, #141E30);
    background-size: cover;
    color: #eee;
    font-family: 'Orbitron', sans-serif;
}

.block-container {
    background-color: rgba(255, 255, 255, 0.05);
    border-radius: 15px;
    padding: 2rem;
    backdrop-filter: blur(8px);
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
}

.chat-bubble {
    padding: 12px 18px;
    border-radius: 20px;
    margin: 12px 0;
    font-size: 15px;
    max-width: 80%;
    transition: all 0.3s ease-in-out;
    animation: floatUp 0.3s ease-in;
}

@keyframes floatUp {
    0% { transform: translateY(10px); opacity: 0; }
    100% { transform: translateY(0); opacity: 1; }
}

.user {
    background: linear-gradient(to right, #1a2a6c, #b21f1f, #fdbb2d);
    color: white;
    align-self: flex-end;
    box-shadow: 0 0 10px #fdbb2d;
}

.bot {
    background: linear-gradient(to left, #00c6ff, #0072ff);
    color: white;
    align-self: flex-start;
    box-shadow: 0 0 10px #0072ff;
}

.message-row {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
}
.message-row.user {
    justify-content: flex-end;
}

.main-header {
    font-size: 38px;
    text-align: center;
    padding: 0.8em;
    margin-bottom: 20px;
}

.neon-gradient-text {
    background: linear-gradient(to right, #ff00cc, #3333ff, #00ffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 15px #00fff7, 0 0 25px #00bfff;
}

.sidebar-box {
    background: rgba(255, 255, 255, 0.04);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 0 12px rgba(0,255,255,0.2);
}
</style>
"""

# === Init user db ===
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

# === USER FUNCTIONS ===
def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

# === CHAT SAVE FUNCTION ===
def save_chat(user_id, chat_log):
    os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)
    fname = f"{user_id}{datetime.datetime.now():%Y%m%d%H%M%S}.json"
    filepath = os.path.join(CHAT_HISTORY_DIR, fname)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(chat_log, f)
    return fname
