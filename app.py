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
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/3f/Logo_example.png", width=200)  # Replace with your SCOUT logo URL
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
    st.image("https://media.istockphoto.com/id/1283120374/photo/elderly-man-falling-down-at-home.jpg?s=612x612&w=0&k=20&c=RrN6N4YfHk3y3ZONy7eWvD1G5M3vA_8pY8mCeS09ooY=", use_column_width=True)
    st.write("Upload a video or image to analyze potential fall incidents.")
    st.file_uploader("Upload a video/image for fall detection", type=["mp4", "avi", "jpg", "png"])
    st.button("Run Detection")

# Fire Detection
elif app_mode == "Fire Detection":
    st.header("🔥 Fire Detection")
    st.image("https://media.istockphoto.com/id/1141047557/photo/fire-in-the-living-room.jpg?s=612x612&w=0&k=20&c=aD27KaZpU_BN5qTj7s3OiPmpwbXme4wQ3Z5A7M6kWl8=", use_column_width=True)
    st.write("Upload a video or image to detect fire hazards.")
    st.file_uploader("Upload a video/image for fire detection", type=["mp4", "avi", "jpg", "png"])
    st.button("Run Detection")

# Intruder Detection
elif app_mode == "Intruder Detection":
    st.header("🕵️ Intruder Detection")
    st.image("https://media.istockphoto.com/id/1354895023/photo/burglar-wearing-black-mask.jpg?s=612x612&w=0&k=20&c=Ac8ZnR9hn-Bt9b4NSEFArYXqLmQe8I_8epn5NR21Smw=", use_column_width=True)
    st.write("Upload a video or image to identify intruders or unauthorized entry.")
    st.file_uploader("Upload a video/image for intruder detection", type=["mp4", "avi", "jpg", "png"])
    st.button("Run Detection")
