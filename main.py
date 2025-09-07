import streamlit as st
import fall_app
import fire_app
import intruder_app

# ✅ Only once here
st.set_page_config(page_title="AI Safety Detection Suite", page_icon="🛡️", layout="wide")

st.sidebar.title("Navigation")
choice = st.sidebar.radio(
    "Choose an App",
    ["Fall Detection", "Fire Detection", "Intruder Detection"]
)

if choice == "Fall Detection":
    fall_app.run()
elif choice == "Fire Detection":
    fire_app.run()
elif choice == "Intruder Detection":
    intruder_app.run()
