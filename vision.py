import os
import cv2
import threading
import time
from deepface import DeepFace

# 🔇 Suppress TensorFlow and GPU logs
# Hide TensorFlow INFO/WARNING
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = ''                    # Disable GPU usage
# Disable oneDNN operation log spam
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# 🔄 Shared emotion state (can be read by main.py or GUI)
emotion_state = {"current": "no_face"}  # Default to no face

# 📸 Load OpenCV's built-in Haar face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# 🧠 Vision loop: runs in the background and updates emotion_state every few seconds


def detect_emotion_if_face_present():
    cam = cv2.VideoCapture(0)  # Use webcam index 0 (face camera)

    if not cam.isOpened():
        print("❌ Webcam not accessible.")
        return

    while True:
        ret, frame = cam.read()
        if not ret:
            continue  # Skip if frame isn't captured properly

        # 🕵️ Step 1: Check for face using Haar cascade
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            # ❌ No face found, skip emotion detection
            emotion_state["current"] = "no_face"
            print("[Vision] 🚫 No face detected.")
        else:
            # ✅ Face found → proceed with DeepFace emotion analysis
            try:
                result = DeepFace.analyze(
                    frame,
                    actions=["emotion"],
                    enforce_detection=False
                )
                emotion = result[0]['dominant_emotion']
                emotion_state["current"] = emotion
                print(f"[Vision] 😊 Emotion Detected: {emotion}")
            except Exception as e:
                print("[Vision] ⚠️ DeepFace error:", e)
                emotion_state["current"] = "error"

        time.sleep(8)  # ⏱ Wait before next check to reduce CPU load

    cam.release()

# 🚀 Call this once from main.py to start the vision thread


def start_observer():
    threading.Thread(target=detect_emotion_if_face_present,
                     daemon=True).start()


# start_observer()

# # Later in your reply logic:
# emotion = emotion_state.get("current", "neutral")

# if emotion == "no_face":
#     print("Jarvis: I can't see you right now.")
# else:
#     print(f"Jarvis: You seem {emotion}. Want help?")
