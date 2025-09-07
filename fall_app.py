import streamlit as st
import cv2
from ultralytics import YOLO
import pandas as pd
import cvzone
import tempfile
import time
from alert import send_alert   # ✅ import your email function

def run():
    st.markdown(
    "<h1 style='text-align: center;'>SCOUT</h1>",
    unsafe_allow_html=True)
    st.title("🛡️ Fall Detection System")



    @st.cache_resource
    def load_model():
        return YOLO(r"runs/detect/train2/weights/best.pt")

    @st.cache_resource
    def load_classes():
        with open("coco.txt", "r") as file:
            return file.read().split("\n")

    model = load_model()
    class_list = load_classes()

    # -----------------------------
    # Detection + Email Alert
    # -----------------------------
    def detect_falls(cap):
        frame_placeholder = st.empty()
        status_placeholder = st.empty()

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        save_path = "fall_detected.avi"
        video_writer = None
        recording = False
        alert_sent = False   # ✅ to avoid multiple emails

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (1020, 600))
            results = model(frame)
            boxes = results[0].boxes.data
            px = pd.DataFrame(boxes.numpy()).astype("float") if boxes is not None else pd.DataFrame()

            fall_detected = False
            for _, row in px.iterrows():
                x1, y1, x2, y2, conf, class_id = map(int, row[:6])
                class_name = class_list[class_id]

                cvzone.putTextRect(frame, f"{class_name}", (x1, y1), 1, 1)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                if class_name == "person":
                    width = x2 - x1
                    height = y2 - y1
                    aspect_ratio = width / height

                    if aspect_ratio > 1.5 and y2 > frame.shape[0] * 0.8:
                        fall_detected = True
                        cvzone.putTextRect(
                            frame, "⚠️ Fall Detected", (50, 50), 2, 2, (0, 0, 255), offset=10, border=3
                        )

            # Save video if fall detected
            if fall_detected:
                if not recording:
                    recording = True
                    video_writer = cv2.VideoWriter(save_path, fourcc, 20.0, (1020, 600))
                video_writer.write(frame)
            else:
                if recording:  # stop recording once fall ends
                    recording = False
                    if video_writer:
                        video_writer.release()
                        video_writer = None
                        # ✅ Send email with saved video
                        if not alert_sent:
                            send_alert(
                                sender_email="shyam451807@gmail.com",
                                sender_password="zuie mfpm zeku jaxp",  # app password
                                recipient_email="ujjwaldwivedi567@gmail.com",
                                video_path=save_path
                            )
                            alert_sent = True

            # Show frame
            frame_placeholder.image(frame, channels="BGR", use_column_width=True)
            if fall_detected:
                status_placeholder.error("⚠️ Fall Detected! Recording...")
            else:
                status_placeholder.info("✅ Monitoring...")

            time.sleep(0.03)

        cap.release()
        if video_writer:
            video_writer.release()

    # -----------------------------
    # UI
    # -----------------------------
    tab1, tab2 = st.tabs(["📂 Upload Video", "📷 Webcam"])

    with tab1:
        video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
        if video_file:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(video_file.read())
            cap = cv2.VideoCapture(tfile.name)
            detect_falls(cap)

    with tab2:
        if st.button("Start Webcam"):
            cap = cv2.VideoCapture(0)
            detect_falls(cap)
