import streamlit as st
import streamlit.components.v1 as components
import json
import os
import requests
import datetime
from settings import THEMES, LANGUAGES, apply_theme
from file_upload import preview_uploaded_file, show_upload_options
from img_generate import generate_ai_image

API_URL = "http://localhost:8000/chat"
USER_DB = "users.json"

if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = ""

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

st.set_page_config(page_title="Chatbot App", layout="centered")
st.title("🤖 Friendly AI Chatbot")

def save_chat(user_id, chat_log):
    os.makedirs("chat_history", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_history/{user_id}_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chat_log, f)
    return filename

def search_chats(user_id, query):
    results = []
    if not os.path.exists("chat_history"):
        return results
    for file in os.listdir("chat_history"):
        if file.startswith(user_id):
            with open(f"chat_history/{file}", "r", encoding="utf-8") as f:
                chat = json.load(f)
                for sender, msg in chat:
                    if query.lower() in msg.lower():
                        results.append((file, sender, msg))
    return results

# === Login/Register Page ===
if not st.session_state.logged_in:
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(to bottom right, #e3f2fd, #ffffff);
                color: #0d47a1;
            }
        </style>
    """, unsafe_allow_html=True)

    menu = st.radio("🔑 Choose option", ["Login", "Register"], horizontal=True)
    users = load_users()

    if menu == "Login":
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        if st.button("🔓 Login"):
            if email in users and users[email] == password:
                st.session_state.logged_in = True
                st.session_state.user_id = email
                st.rerun()
            else:
                st.error("❌ Invalid credentials.")
    else:
        email = st.text_input("📧 New Email")
        password = st.text_input("🔑 Password", type="password")
        confirm = st.text_input("✅ Confirm Password", type="password")
        if st.button("📝 Register"):
            if email in users:
                st.warning("⚠️ User exists.")
            elif password != confirm:
                st.warning("❗ Passwords mismatch.")
            elif not email or not password:
                st.warning("Please fill all fields.")
            else:
                users[email] = password
                save_users(users)
                st.success("🎉 Registered! Login now.")

# === Main Chat UI ===
else:
    with st.sidebar:
        st.markdown("### 💬 Chatbot Menu")

        theme = st.selectbox("🎨 Select Theme", list(THEMES.keys()), index=0)
        language = st.selectbox("🌐 Language", LANGUAGES, index=0)
        apply_theme(theme)

        if st.button("📝 New Chat"):
            save_chat(st.session_state.user_id, st.session_state.chat_log)
            st.session_state.chat_log = []
            st.rerun()

        if st.button("🔍 Search Chats"):
            term = st.text_input("Search:", key="search_term")
            if term:
                results = search_chats(st.session_state.user_id, term)
                for file, sender, msg in results:
                    st.markdown(f"📁 **{file}** — **{sender}**: {msg}")

        if st.button("📤 Save Chat"):
            filename = save_chat(st.session_state.user_id, st.session_state.chat_log)
            st.success(f"✅ Saved: {filename}")

        if st.button("🔒 Logout"):
            save_chat(st.session_state.user_id, st.session_state.chat_log)
            st.session_state.logged_in = False
            st.session_state.user_id = ""
            st.session_state.chat_log = []
            st.rerun()

    st.subheader(f"👋 Hello, [{st.session_state.user_id}](mailto:{st.session_state.user_id})!")
    st.caption(f"🌐 Chatting in: **{language}**")

    # === Chat Input Row: Input + "+" + ⬆️ ===
    col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
    with col1:
        user_input = st.text_input("Type your message here", placeholder="Type your message here...", label_visibility="collapsed")
    with col2:
        show_upload_options()
    with col3:
        if st.button("⬆️", key="send_btn") and user_input.strip():
            st.session_state.chat_log.append(("👤 You", user_input))
            st.session_state.pending_prompt = user_input
            st.rerun()

    # === Display Chat History + Thinking Spinner ===
    if st.session_state.chat_log:
        st.subheader("📜 Chat History")
        for sender, msg in st.session_state.chat_log:
            bubble = f"<div style='padding:10px;margin:5px 0;border-radius:10px;background:#f1f1f1'><b>{sender}:</b> {msg}</div>"
            st.markdown(bubble, unsafe_allow_html=True)

    # === If AI is pending, show spinner inside chat and process ===
    if "pending_prompt" in st.session_state:
        st.session_state.chat_log.append(("🤖 AI", "🤖 Thinking..."))
        st.rerun()

    if st.session_state.chat_log and st.session_state.chat_log[-1][1] == "🤖 Thinking...":
        try:
            prompt = f"Please respond in {language} only:\n\n{st.session_state.pending_prompt}"
            response = requests.post(API_URL, json={"prompt": prompt})
            reply = response.json().get("response", "(No reply)")
        except Exception as e:
            reply = f"(Server error): {e}"

        st.session_state.chat_log.pop()  # remove "Thinking..."
        st.session_state.chat_log.append(("🤖 AI", reply))
        del st.session_state.pending_prompt
        st.rerun()
