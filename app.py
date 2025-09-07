import streamlit as st

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
    st.header("Welcome to SCOUT 🚀")
    st.image("https://images.unsplash.com/photo-1581090700227-4c4f50b6d2d6", use_column_width=True)
    st.write("""
    This is a demo frontend for the SCOUT project.  
    Use the sidebar to navigate between modules:
    - 🧍 Fall Detection  
    - 🔥 Fire Detection  
    - 🕵️ Intruder Detection  
    """)

    st.info("⚠️ Note: This is frontend-only. Model functionality is not included.")

# Fall Detection
elif app_mode == "Fall Detection":
    st.header("🧍 Fall Detection")
    st.image("https://images.unsplash.com/photo-1603398938378-8d3d3f8cbf53", use_column_width=True)
    st.write("This page is for fall detection functionality.")
    st.file_uploader("Upload a video/image for fall detection", type=["mp4", "avi", "jpg", "png"])
    st.button("Run Detection")

# Fire Detection
elif app_mode == "Fire Detection":
    st.header("🔥 Fire Detection")
    st.image("https://images.unsplash.com/photo-1503376780353-7e6692767b70", use_column_width=True)
    st.write("This page is for fire detection functionality.")
    st.file_uploader("Upload a video/image for fire detection", type=["mp4", "avi", "jpg", "png"])
    st.button("Run Detection")

# Intruder Detection
elif app_mode == "Intruder Detection":
    st.header("🕵️ Intruder Detection")
    st.image("https://images.unsplash.com/photo-1556740749-887f6717d7e4", use_column_width=True)
    st.write("This page is for intruder detection functionality.")
    st.file_uploader("Upload a video/image for intruder detection", type=["mp4", "avi", "jpg", "png"])
    st.button("Run Detection")
