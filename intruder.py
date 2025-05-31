import cv2
import face_recognition
import os
import numpy as np
from capture import camerafeed
from datetime import datetime, timedelta

# Load known face encodings
def load_known_faces(known_folder):
    known_encodings = []
    known_names = []

    for filename in os.listdir(known_folder):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            image_path = os.path.join(known_folder, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:  # If encodings are found
                known_encodings.append(encodings[0])
                known_names.append(os.path.splitext(filename)[0])
    return known_encodings, known_names

# Variables
known_folder = "known_faces"
known_encodings, known_names = load_known_faces(known_folder)

# Initialize video capture
cap = cv2.VideoCapture(0)  # Use 0 for webcam or a video file path
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for saving video

recording = False
out = None
unknown_threshold = 5  # Seconds to wait before stopping recording
last_unknown_time = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    unknown_detected = False

    for face_encoding in face_encodings:
        # Compare with known faces
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
        else:
            unknown_detected = True

    # Handle recording logic
    current_time = datetime.now()
    if unknown_detected:
        if not recording:
            # Start recording
            recording = True
            out = cv2.VideoWriter(f"recording_{current_time.strftime('%Y%m%d_%H%M%S')}.avi", fourcc, 20.0, (frame.shape[1], frame.shape[0]))
            print("Recording started...")
        last_unknown_time = current_time
    elif recording:
        # Stop recording if no unknown faces for threshold time
        if last_unknown_time and (current_time - last_unknown_time > timedelta(seconds=unknown_threshold)):
            recording = False
            out.release()
            print("Recording stopped...")

    # Write the frame to the video file if recording
    if recording and out:
        out.write(frame)

    # Display the video feed
    cv2.imshow("Camera Feed", frame)

    # Quit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
if recording and out:
    out.release()
cap.release()
cv2.destroyAllWindows()