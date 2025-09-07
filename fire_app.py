import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import traceback
import streamlit as st
import cv2
from ultralytics import YOLO
import cvzone
import tempfile


# -----------------------------
# Email Sending Function
# -----------------------------
def send_alert(sender_email, sender_password, recipient_email, image_path):
    """
    Sends an email alert with a snapshot attachment.
    """
    try:
        if not os.path.exists(image_path):
            print(f"❌ Error: The image file '{image_path}' does not exist.")
            return

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "🔥 Fire Detected Alert - Snapshot"
        body = (
            "Dear User,\n\n"
            "A fire was detected by your monitoring system. "
            "Please find the attached snapshot for review.\n\n"
            "Best regards,\nYour Security System"
        )
        msg.attach(MIMEText(body, 'plain'))

        # Attach snapshot
        with open(image_path, "rb") as file:
            mime_base = MIMEBase('application', 'octet-stream')
            mime_base.set_payload(file.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(image_path)}'
            )
            msg.attach(mime_base)

        print("📧 Connecting to SMTP server...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("✅ Email alert sent successfully!")

    except Exception as e:
        print(f"❌ Error sending email alert: {e}")
        print(traceback.format_exc())


# -----------------------------
# Fire Detection Function
# -----------------------------
def detect_fire(video_path=None, use_webcam=False):
    model = YOLO(r"C:\Users\ujjwa\OneDrive\Desktop\SCOUT\runs\detect\train\weights\best.pt")

    if use_webcam:
        cap = cv2.VideoCapture(0)  # webcam
    else:
        cap = cv2.VideoCapture(video_path)  # video file

    frame_count = 0
    save_path = "fire_detected.jpg"
    email_sent = False   # <--- flag

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        if frame_count % 3 != 0:
            continue

        results = model(frame, conf=0.05)
        fire_detected = False

        if results[0].boxes is not None and len(results[0].boxes) > 0:
            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = model.names[class_id]

                fire_detected = True

                # Save snapshot once
                if not email_sent:
                    cv2.imwrite(save_path, frame)
                    send_alert(
                        sender_email="shyam451807@gmail.com",
                        sender_password="zuie mfpm zeku jaxp",
                        recipient_email="ujjwaldwivedi567@gmail.com",
                        image_path=save_path
                    )
                    print("📸 Fire detected! Snapshot emailed.")
                    email_sent = True   # <--- prevent more emails
                break

        yield frame  # to display in Streamlit/UI

    cap.release()
    cv2.destroyAllWindows()
# -----------------------------
# Fire Detection App
# -----------------------------
def run():
    st.markdown("<h1 style='text-align: center;'>SCOUT</h1>", unsafe_allow_html=True)
    st.title("🔥 Fire Detection System")

    @st.cache_resource
    def load_model():
        return YOLO(r"C:\Users\ujjwa\OneDrive\Desktop\SCOUT\runs\detect\train\weights\best.pt")

    global model
    model = load_model()

    st.markdown("Upload a video or use webcam to detect fire incidents in real-time using YOLO 🚨")

    tab1, tab2 = st.tabs(["📂 Upload Video", "📷 Webcam"])

    # Upload Video Tab
    with tab1:
        video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
        if video_file is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(video_file.read())
            video_path = tfile.name

            stframe = st.empty()
            status_placeholder = st.empty()

            for frame in detect_fire(video_path, use_webcam=False):
                stframe.image(frame, channels="BGR", use_column_width=True)
                status_placeholder.info("🔍 Detecting fire...")

            status_placeholder.success("✅ Detection finished.")

    # Webcam Tab
    with tab2:
        if st.button("Start Webcam Fire Detection"):
            stframe = st.empty()
            status_placeholder = st.empty()

            for frame in detect_fire(0, use_webcam=True):
                stframe.image(frame, channels="BGR", use_column_width=True)
                status_placeholder.info("🎥 Webcam active - detecting fire...")