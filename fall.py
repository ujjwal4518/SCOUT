import cv2
from ultralytics import YOLO
import pandas as pd
import cvzone

# Load YOLO model
model = YOLO(r"C:\Users\ujjwa\OneDrive\Desktop\SCOUT\runs\detect\train2\weights\best.pt")

# Load COCO class labels
with open(r"coco.txt", "r") as file:
    class_list = file.read().split("\n")

def detect_falls():
    """Generator function for video processing, streaming, and recording falls."""
    cap = cv2.VideoCapture(r"C:\Users\ujjwa\OneDrive\Desktop\WhatsApp Video 2024-11-19 at 16.37.09_259d4a8a.mp4")
    #
    frame_count = 0
    recording = False
    video_writer = None
    save_path = "fall_detected.avi"  # File path for saving the video

    # Define video writer properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    while True:
        ret, frame = cap.read()
        frame_count += 1

        if not ret:
            break

        # Skip frames for performance
        if frame_count % 3 != 0:
            continue

        # Resize frame
        frame = cv2.resize(frame, (1020, 600))

        # Run YOLO model for detection
        results = model(frame)
        boxes = results[0].boxes.data
        px = pd.DataFrame(boxes.numpy()).astype("float") if boxes is not None else pd.DataFrame()

        fall_detected = False

        for index, row in px.iterrows():
            x1, y1, x2, y2, conf, class_id = map(int, row[:6])
            class_name = class_list[class_id]

            cvzone.putTextRect(frame, f"{class_name}", (x1, y1), 1, 1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if class_name == "person":
                width = x2 - x1
                height = y2 - y1
                aspect_ratio = width / height

                # Fall detection logic
                if aspect_ratio > 1.5 and y2 > frame.shape[0] * 0.8:
                    fall_detected = True
                    cvzone.putTextRect(
                        frame, "Fall Detected", (50, 50), 2, 2, (0, 0, 255), offset=10, border=3
                    )

        # Start recording if a fall is detected
        if fall_detected:
            if not recording:
                recording = True
                video_writer = cv2.VideoWriter(save_path, fourcc, 20.0, (1020, 600))
            video_writer.write(frame)

        # Stop recording if no falls are detected
        if recording and not fall_detected:
            recording = False
            if video_writer:
                video_writer.release()
                video_writer = None

        # Encode frame as JPEG for streaming
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Release resources
    cap.release()
    if video_writer:
        video_writer.release()