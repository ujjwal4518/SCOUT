import numpy as np
import cv2

# Webcam capture
def webcam():
    cap = cv2.VideoCapture(0)  # Open default webcam
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None
    return cap

# Local video file capture
def localvideo():
    cap = cv2.VideoCapture(r"sample\pred_fire-forest_4.mp4")  # Video file path
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return None
    return cap

# YouTube video capture (via pafy)

# DroidCam capture (from a mobile device)
def droidcam():
    cap = cv2.VideoCapture('http://192.168.0.102:4747/mjpegfeed')  # DroidCam URL
    if not cap.isOpened():
        print("Error: Could not connect to DroidCam.")
        return None
    return cap

# RTSP stream
def camerafeed():
    cap = cv2.VideoCapture()
    cap.open("rtsp://USER:PASS@IP:PORT/Streaming/Channels/2")  # RTSP feed URL
    if not cap.isOpened():
        print("Error: Could not connect to live feed.")
        return None
    return cap
