import streamlit as st
from pathlib import Path

# Set base path for images
BASE_DIR = Path(__file__).parent / "images"

# Page setup
st.set_page_config(page_title="SCOUT - Safety Monitoring", layout="wide")
st.title("🛡️ SCOUT - Safety Monitoring Dashboard")

# Sidebar navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio(
    "Choose a module:",
    ["Home", "Fall Detection", "Fire Detection", "Intruder Detection"]
)

# Home Page
if app_mode == "Home":
    st.image(str(BASE_DIR / "logo.png"), width=200)
    st.header("Welcome to SCOUT 🚀")
    st.write("""
    **SCOUT** is an AI-powered safety monitoring system designed to detect:
    - 🧍 Falls  
    - 🔥 Fires  
    - 🕵️ Intruders  

    Use the sidebar to navigate between modules.
    """)

# Fall Detection
elif app_mode == "Fall Detection":
    st.header("🧍 Fall Detection")
    st.image(str(BASE_DIR / "fall.jpg"), use_column_width=True)
    st.write("Upload a video or image to analyze potential fall incidents.")
    st.file_uploader("Upload a video/image for fall detection", type=["mp4", "avi", "jpg", "png"])
    st.button("Run Detection")

# Fire Detection
elif app_mode == "Fire Detection":
    st.header("🔥 Fire Detection")
    st.image(str(BASE_DIR / "fire.jpg"), use_column_width=True)
    st.write("Upload a video or image to detect fire hazards.")
    st.file_uploader("Upload a video/image for fire detection", type=["mp4", "avi", "jpg", "png"])
    st.button("Run Detection")

# Intruder Detection
elif app_mode == "Intruder Detection":
    st.header("🕵️ Intruder Detection")
    st.image(str(BASE_DIR / "intruder.jpg"), use_column_width=True)
    st.write("Upload a video or image to identify intruders or unauthorized entry.")
    st.file_uploader("Upload a video/image for intruder detection", type=["mp4", "avi", "jpg", "png"])
    st.button("Run Detection")
