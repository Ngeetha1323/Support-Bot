import streamlit as st
import requests

def generate_ai_image():
    image_url = "https://placekitten.com/400/300"  # Replace this with your own model API
    st.image(image_url, caption="🎨 AI Generated Image")