import os
import time
from pathlib import Path
import streamlit as st
import cv2
from typing import Optional, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Optional import of ultralytics YOLO
try:
    from ultralytics import YOLO
    _ULTRA_OK = True
except Exception:
    _ULTRA_OK = False

st.set_page_config(page_title="SCOUT – Unified Safety Dashboard", layout="wide")

# ---------- Helpers ----------
def load_model(weights_path: Optional[str]):
    if not _ULTRA_OK:
        st.error("ultralytics not installed. Add it to requirements.txt and deploy again.")
        return None
    if not weights_path or not os.path.exists(weights_path):
        st.warning("Weights file not found. Using built-in YOLO model (yolov8n.pt).")
        return YOLO("yolov8n.pt")
    return YOLO(weights_path)

def open_video(source: str):
    if source == "0":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        st.error("Could not open video source.")
        return None
    return cap

# ---------- Email ----------
def send_email_alert(subject: str, body: str):
    if not enable_email or not sender_email or not sender_pass or not recipient_email:
        return
    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_pass)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        st.sidebar.success(f"📧 Email sent: {subject}")
    except Exception as e:
        st.sidebar.error(f"Email failed: {e}")

def send_alert_generic(event: str, detail: str = ""):
    st.toast(f"ALERT: {event} {detail}", icon="🚨")
    send_email_alert(f"SCOUT Alert: {event}", f"{event} detected at {time.ctime()}\n\nDetails: {detail}")

# ---------- UI ----------
st.sidebar.title("SCOUT")
st.sidebar.caption("Unified Streamlit App")

mode = st.sidebar.selectbox("Select Feature", ["Home", "Fire Detection", "Fall Detection", "Intruder Detection"])
st.sidebar.markdown("---")
st.sidebar.subheader("Model Weights")
fire_w = st.sidebar.text_input("Fire weights path", value="best.pt")
fall_w = st.sidebar.text_input("Fall weights path", value="best.pt")
intr_w = st.sidebar.text_input("Intruder weights path", value="best.pt")
st.sidebar.markdown("---")
default_source = st.sidebar.text_input("Video source (file path, URL, or 0 for webcam)", value="0")
conf = st.sidebar.slider("Confidence threshold", 0.1, 0.9, 0.5, 0.05)

# ---------- Email Settings ----------
st.sidebar.markdown("---")
st.sidebar.subheader("Email Alerts")
enable_email = st.sidebar.checkbox("Enable email alerts")
smtp_server = st.sidebar.text_input("SMTP server", value="smtp.gmail.com")
smtp_port = st.sidebar.number_input("SMTP port", value=587)
sender_email = st.sidebar.text_input("Sender email")
sender_pass = st.sidebar.text_input("Sender password / App password", type="password")
recipient_email = st.sidebar.text_input("Recipient email")

st.title("🛡️ SCOUT – Unified Safety Dashboard")

if mode == "Home":
    st.markdown(
        """
        Use the sidebar to select a feature.  

        ✅ Fire Detection → Alerts when YOLO finds **fire/smoke**  
        ✅ Fall Detection → Alerts when YOLO finds a **fall class**  
        ✅ Intruder Detection → Alerts when YOLO finds a **person**  
        ✅ Email Alerts → Optional SMTP email notification for critical detections  
        """
    )

# ---------- Run Feature ----------
def run_detection(name: str, weights: str, targets: Optional[List[str]]):
    st.header(name)

    uploaded = st.file_uploader("Optionally upload a video file", type=["mp4", "mov", "avi", "mkv"])
    src = default_source
    tmpfile = None
    if uploaded is not None:
        tmpfile = Path(f"uploaded_{int(time.time())}.mp4")
        with open(tmpfile, "wb") as fh:
            fh.write(uploaded.read())
        src = str(tmpfile)

    model = load_model(weights)
    if model is None:
        return

    st.sidebar.text(f"Loaded classes: {list(model.names.values())}")

    cap = open_video(src)
    if cap is None:
        return

    placeholder = st.empty()
    run = st.toggle("Start", value=True)

    while cap.isOpened() and run:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=conf, verbose=False)

        detected_labels = []
        for r in results:
            for b in r.boxes:
                cls_id = int(b.cls[0])
                label = model.names.get(cls_id, str(cls_id))
                detected_labels.append(label.lower())
                x1, y1, x2, y2 = map(int, b.xyxy[0].tolist())
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Debug sidebar
        st.sidebar.write("Detections:", detected_labels)

        # --- Alerts ---
        if name == "Fire Detection" and any(lbl in ["fire", "smoke"] for lbl in detected_labels):
            send_alert_generic("🔥 Fire Detected")
            cv2.putText(frame, "FIRE DETECTED!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

        elif name == "Fall Detection" and any("fall" in lbl for lbl in detected_labels):
            send_alert_generic("🧍‍♂️ Fall Detected")
            cv2.putText(frame, "FALL DETECTED!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

        elif name == "Intruder Detection" and "person" in detected_labels:
            send_alert_generic("🚶 Intruder Detected")
            cv2.putText(frame, "INTRUDER DETECTED!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

        # Show frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        placeholder.image(frame_rgb, channels="RGB", use_column_width=True)

    cap.release()
    if tmpfile and Path(tmpfile).exists():
        Path(tmpfile).unlink(missing_ok=True)

# ---------- Mode Routing ----------
if mode == "Fire Detection":
    run_detection("Fire Detection", fire_w, targets=["fire", "smoke"])

elif mode == "Fall Detection":
    run_detection("Fall Detection", fall_w, targets=["fall"])

elif mode == "Intruder Detection":
    run_detection("Intruder Detection", intr_w, targets=["person"])
