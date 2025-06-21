import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = "your-api-key-here"  # Replace with your actual API key

# Function to get reply from GPT
def get_gpt_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response['choices'][0]['message']['content']

# Function to load external CSS
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load external CSS file
load_css("style.css")

# Configure Streamlit page
st.set_page_config(page_title="Fancy AI Chatbot", layout="centered")
st.markdown("<h2 style='text-align: center;'>Fancy AI Chatbot</h2>", unsafe_allow_html=True)

# Clear Chat Button
if st.button("Clear Chat"):
    st.session_state.chat_history = []

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input from user
user_input = st.text_input("You:", key="ai_input_field", label_visibility="collapsed")

# Process user input
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    ai_reply = get_gpt_response(user_input)
    st.session_state.chat_history.append(("bot", ai_reply))

# Display messages as chat bubbles
for sender, message in st.session_state.chat_history:
    bubble_class = "user-bubble" if sender == "user" else "bot-bubble"
    st.markdown(f"<div class='chat-container'><div class='chat-bubble {bubble_class}'>{message}</div></div>", unsafe_allow_html=True)
