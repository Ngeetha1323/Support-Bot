import streamlit as st
import requests

THEMES = {
    "Soft Gradient": """
        <style>
        .stApp {
            background: linear-gradient(135deg, #b3ffab 0%, #12fff7 100%);
            font-family: 'Segoe UI', sans-serif;
        }
        </style>
    """,
    "Dark Mode": """
        <style>
        .stApp {
            background-color: #121212;
            color: white;
        }
        </style>
    """,
    "Peach Warm": """
        <style>
        .stApp {
            background: linear-gradient(135deg, #FFD3A5 0%, #FD6585 100%);
            color: black;
        }
        </style>
    """
}

LANGUAGES = ["English", "Tamil", "Hindi", "French", "Spanish"]

def apply_theme(theme_name):
    if theme_name in THEMES:
        st.markdown(THEMES[theme_name], unsafe_allow_html=True)

def load_lottie_url(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None

def inject_login_css():
    st.markdown("""
    <style>
    .login-box {
        padding: 2rem;
        margin-top: 0.5rem;
    }

    h1, .stRadio > label {
        color: #1f2937;
        font-weight: bold;
    }

    .stTextInput > div > input,
    .stTextArea textarea {
        background-color: #f3f4f6;
        border: 1px solid #cbd5e0;
        border-radius: 8px;
    }

    .stButton > button {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        border: none;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
