# file_upload.py

import streamlit as st
from PIL import Image

def preview_uploaded_file(uploaded_file):
    if uploaded_file:
        file_details = {
            "filename": uploaded_file.name,
            "type": uploaded_file.type,
            "size": uploaded_file.size
        }
        st.write("### File Info:", file_details)

        if uploaded_file.type.startswith("text"):
            content = uploaded_file.read().decode("utf-8")
            st.text_area("📄 File Content", content, height=200)
        elif uploaded_file.type.startswith("image"):
            st.image(uploaded_file, caption="🖼 Uploaded Image", use_column_width=True)
        else:
            st.info("✅ File uploaded. No preview available.")

def show_upload_options():
    with st.popover("➕", use_container_width=False):
        st.markdown("### 📸 Take Photo")
        st.file_uploader(" ", type=["jpg", "jpeg", "png"], key="take_photo", label_visibility="collapsed")

        st.markdown("### 🖼 Add Photo")
        st.file_uploader(" ", type=["jpg", "jpeg", "png"], key="add_photo", label_visibility="collapsed")

        st.markdown("### 📁 Add File")
        st.file_uploader(" ", type=["txt", "pdf", "docx", "csv", "json"], key="add_file", label_visibility="collapsed")
