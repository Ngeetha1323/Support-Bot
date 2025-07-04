import streamlit as st
import json
import os
import requests
import datetime
from setting import THEMES, LANGUAGES, apply_theme, load_lottie_url, inject_login_css
from streamlit_lottie import st_lottie

# ==== CONFIG ====
API_URL = "http://localhost:8000/chat"
USER_DB = "users.json"
st.set_page_config(page_title="Chatbot App", layout="centered")

# Load Lottie animation
lottie_animation = load_lottie_url("https://lottie.host/2e578582-5b3d-4c10-9709-d1672dfac13a/lv6GASw1hV.json")

# Inject CSS
inject_login_css()

# ==== SESSION INIT ====
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = ""

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# ==== USER DB ====
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f)

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

# ==== UI ====
if not st.session_state.logged_in:
    apply_theme("Soft Gradient")

    st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
    if lottie_animation:
        st_lottie(lottie_animation, height=200, key="girl")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.title("🔐 Login or Register")
    menu = st.radio("Choose option", ["Login", "Register"], horizontal=True)
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
    st.markdown("</div>", unsafe_allow_html=True)

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
                    st.markdown(f"📁 *{file}* — *{sender}*: {msg}")

        if st.button("📤 Save Chat"):
            filename = save_chat(st.session_state.user_id, st.session_state.chat_log)
            st.success(f"✅ Saved: {filename}")

        if st.button("🔒 Logout"):
            save_chat(st.session_state.user_id, st.session_state.chat_log)
            st.session_state.logged_in = False
            st.session_state.user_id = ""
            st.session_state.chat_log = []
            st.rerun()

    st.subheader(f"👋 Hello, {st.session_state.user_id}!")
    st.caption(f"🌐 Chatting in: *{language}*")

    user_input = st.text_area("📝 Your question:")
    if st.button("🚀 Ask") and user_input.strip():
        with st.spinner("🤖 Thinking..."):
            try:
                prompt = f"Please respond in {language} only:\n\n{user_input}"
                response = requests.post(API_URL, json={"prompt": prompt})
                reply = response.json().get("response", "(No reply)")
            except Exception as e:
                reply = f"(Server error): {e}"

        st.session_state.chat_log.append(("👤 You", user_input))
        st.session_state.chat_log.append(("🤖 AI", reply))

    if st.session_state.chat_log:
        st.subheader("📜 Chat History")
        for sender, msg in st.session_state.chat_log:
            bubble = f"<div style='padding:10px;margin:5px 0;border-radius:10px;background:#f1f1f1'><b>{sender}:</b> {msg}</div>"
            st.markdown(bubble, unsafe_allow_html=True)
