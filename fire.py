import cv2
from ultralytics import YOLO
import cvzone

# Load YOLO model
model = YOLO(r"C:\Users\ujjwa\OneDrive\Desktop\SCOUT\runs\detect\train\weights\best.pt")

with open(r"coco.txt", "r") as file:
    class_list = file.read().split("\n")
    
# Define fire detection function
def detect_fire():
    """Generator function for video processing, streaming, and recording fire detection."""
    cap = cv2.VideoCapture(r"sample\pred_fire-forest_4.mp4")  # Replace with your video path
    frame_count = 0
    recording = False
    video_writer = None
    save_path = "fire_detected.avi"  # File path for saving the video

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
        fire_detected = False

        if boxes is not None:
            for box in boxes:
                x1, y1, x2, y2, conf, class_id = map(int, box[:6])
                class_name = model.names[class_id]

                # Draw bounding box and label
                cvzone.putTextRect(frame, f"{class_name} {conf:.2f}", (x1, y1), 1, 1, colorR=(0, 0, 255))
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                # Check for fire detection
                if class_name.lower() == "fire":
                    fire_detected = True

        # Start recording if fire is detected
        if fire_detected:
            if not recording:
                recording = True
                print("Fire detected! Starting recording...")
                video_writer = cv2.VideoWriter(save_path, fourcc, 20.0, (1020, 600))
            video_writer.write(frame)

        # Stop recording if no fire is detected
        if recording and not fire_detected:
            recording = False
            if video_writer:
                video_writer.release()
                print("Recording stopped. Video saved.")

        # Encode frame as JPEG for streaming
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Release resources
    cap.release()
    if video_writer:
        video_writer.release()
    print("All resources released.")
