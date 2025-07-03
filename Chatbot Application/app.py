import streamlit as st
import requests
import os
import json
from setting import load_users, save_users, save_chat, CHATBOT_CSS

# Page config
st.set_page_config(page_title="🤖 AI ChatBot", layout="wide")
st.markdown(CHATBOT_CSS, unsafe_allow_html=True)

MISTRAL_API_KEY = "crJ3S6ZZkKRI4wIsykWaPd0sL4RmHnVD"
API_URL = "https://api.mistral.ai/v1/chat/completions"

# Session init
for key, default in [
    ("logged_in", False),
    ("user_id", ""),
    ("chat_log", []),
    ("pending_prompt", None),
    ("theme", "light"),
    ("language", "English"),
]:
    if key not in st.session_state:
        st.session_state[key] = default

def load_chats(user_id):
    folder = "chats"
    os.makedirs(folder, exist_ok=True)
    user_file = os.path.join(folder, f"{user_id}_chats.json")
    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            return json.load(f)
    return []

# -------- LOGIN PAGE ----------
if not st.session_state.logged_in:
    users = load_users()
    st.markdown("<div class='login-box neon-box'><h2>🔐 Login or Register</h2></div>", unsafe_allow_html=True)
    mode = st.radio("Select Mode", ["Login", "Register"], horizontal=True)
    email = st.text_input("Email")
    pwd = st.text_input("Password", type="password")

    if mode == "Login":
        if st.button("Login", use_container_width=True):
            if users.get(email) == pwd:
                st.session_state.logged_in = True
                st.session_state.user_id = email
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials.")
    else:
        confirm = st.text_input("Confirm password", type="password")
        if st.button("Register", use_container_width=True):
            if email in users:
                st.warning("⚠️ User already exists.")
            elif not email or pwd != confirm:
                st.warning("⚠️ Fill all fields correctly.")
            else:
                users[email] = pwd
                save_users(users)
                st.success("🎉 Registered! Please login.")

# -------- CHAT PAGE ----------
else:
    st.markdown("<div class='main-header neon-gradient-text'> 🤖 Support ChatBot</div>", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<div class='sidebar-box neon-box'>", unsafe_allow_html=True)
        st.header("⚙️ Settings")

        if st.button("✨ New Chat", use_container_width=True):
            save_chat(st.session_state.user_id, st.session_state.chat_log)
            st.session_state.chat_log = []
            st.rerun()

        if st.button("🧹 Clear Chat", use_container_width=True):
            st.session_state.chat_log = []
            st.rerun()

        chats = load_chats(st.session_state.user_id)
        chat_titles = [" > ".join(msg[1][:30].split()[:5]) + "..." if msg else "(Empty)" for chat in chats for msg in chat[:1]]
        if chat_titles:
            selected_index = st.selectbox("📁 Old Chats", range(len(chats)), format_func=lambda i: chat_titles[i])
            if chats:
                st.session_state.chat_log = chats[selected_index]
                st.success("Loaded old chat!")

        st.text_input("🔍 Search in Chats")
        st.selectbox("🎨 Theme", ["light", "dark"], key="theme")
        st.selectbox("🌐 Language", ["English", "தமிழ்", "हिंदी"], key="language")

        if st.button("🚪 Logout", use_container_width=True):
            save_chat(st.session_state.user_id, st.session_state.chat_log)
            st.session_state.logged_in = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    user_input = st.text_input("Ask me anything...")
    if st.button("Send", use_container_width=True) and user_input.strip():
        st.session_state.chat_log.append(("You", user_input))
        st.session_state.chat_log.append(("AI", "Thinking..."))
        st.session_state.pending_prompt = user_input
        st.rerun()

    for sender, msg in st.session_state.chat_log:
        role = "user" if sender == "You" else "bot"
        row_class = "message-row user" if role == "user" else "message-row"
        bubble_class = f"chat-bubble {role} neon-bubble"
        st.markdown(f'<div class="{row_class}"><div class="{bubble_class}">{msg}</div></div>', unsafe_allow_html=True)

    if st.session_state.pending_prompt:
        with st.spinner("Bot is thinking…"):
            try:
                headers = {
                    "Authorization": f"Bearer {MISTRAL_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "mistral-medium",
                    "messages": [{"role": "user", "content": st.session_state.pending_prompt}]
                }
                response = requests.post(API_URL, headers=headers, json=payload)
                response.raise_for_status()
                result = response.json()
                reply = result["choices"][0]["message"]["content"].strip()
            except Exception as e:
                reply = f"(Error): {e}"

        st.session_state.chat_log.pop()
        st.session_state.chat_log.append(("AI", reply))
        st.session_state.pending_prompt = None
        st.rerun()
