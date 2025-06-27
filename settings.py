# settings.py

THEMES = {
    "Soft Gradient": """
        <style>
            .stApp {
                background: linear-gradient(to bottom right, #e3f2fd, #ffffff);
                color: #0d47a1;
            }
        </style>
    """,
    "Dark Night": """
        <style>
            .stApp {
                background: linear-gradient(to right, #232526, #414345);
                color: white;
            }
            input, textarea {
                background-color: #2c3e50 !important;
                color: white !important;
            }
        </style>
    """,
    "Purple & Pink": """
        <style>
            .stApp {
                background: linear-gradient(to right, #cc2b5e, #753a88);
                color: white;
            }
        </style>
    """
}

LANGUAGES = ["English", "Tamil", "Hindi", "French"]

def apply_theme(theme_name):
    import streamlit as st
    css = THEMES.get(theme_name, "")
    if css:
        st.markdown(css, unsafe_allow_html=True)
