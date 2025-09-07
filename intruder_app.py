import streamlit as st
import cv2
import face_recognition
import os
from datetime import datetime
import tempfile
import time

# Import intruder alert function
from alert_intruder import send_intruder_alert


def run():
    st.markdown(
        "<h1 style='text-align: center;'>SCOUT</h1>",
        unsafe_allow_html=True
    )
    st.title("🕵‍♂ Intruder Detection System")

    # -----------------------------
    # Load Known Faces
    # -----------------------------
    @st.cache_resource
    def load_known_faces(known_folder):
        known_encodings = []
        known_names = []
        for filename in os.listdir(known_folder):
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                image_path = os.path.join(known_folder, filename)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_encodings.append(encodings[0])
                    known_names.append(os.path.splitext(filename)[0])
        return known_encodings, known_names

    known_folder = "known_faces"
    known_encodings, known_names = load_known_faces(known_folder)

    # -----------------------------
    # Detection Function
    # -----------------------------
    def detect_intruders(video_path, from_webcam=False):
        cap = cv2.VideoCapture(video_path if not from_webcam else 0)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        intruder_alert_sent = False
        recorded_file = "intruder.avi"

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            unknown_detected = False

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]

                # Draw box & name
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                if name == "Unknown":
                    unknown_detected = True
                    cv2.putText(frame, "🚨 Intruder Detected 🚨", (50, 50),
                                cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 255), 3)

            if unknown_detected and not intruder_alert_sent:
                # Start recording 5 seconds
                out = cv2.VideoWriter(recorded_file, fourcc, 20.0, (frame.shape[1], frame.shape[0]))

                start_time = time.time()
                while time.time() - start_time < 5:
                    ret2, frame2 = cap.read()
                    if not ret2:
                        break
                    out.write(frame2)
                out.release()

                # Send email alert with recorded file
                send_intruder_alert(
                    sender_email="shyam451807@gmail.com",
                    sender_password="zuie mfpm zeku jaxp",  # App password
                    recipient_email="ujjwaldwivedi567@gmail.com",
                    video_path=recorded_file
                )

                intruder_alert_sent = True

            yield frame

        cap.release()

    # -----------------------------
    # Streamlit Frontend
    # -----------------------------
    st.markdown("This app detects unknown intruders using face recognition. 🚨")

    tab1, tab2 = st.tabs(["📂 Upload Video", "📷 Webcam"])

    with tab1:
        video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
        if video_file is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(video_file.read())
            video_path = tfile.name

            stframe = st.empty()
            status_placeholder = st.empty()

            for frame in detect_intruders(video_path, from_webcam=False):
                stframe.image(frame, channels="BGR", use_column_width=True)
                status_placeholder.info("🔍 Detecting intruders...")

            status_placeholder.success("✅ Detection finished.")

    with tab2:
        if st.button("Start Webcam"):
            stframe = st.empty()
            status_placeholder = st.empty()

            for frame in detect_intruders(None, from_webcam=True):
                stframe.image(frame, channels="BGR", use_column_width=True)
                status_placeholder.info("📡 Live detection running...")