import cv2
import time
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# =========================
# CONFIG
# =========================
VIDEO_PATH = os.path.join("assets", "skyrim-skeleton.mp4")
MODEL_PATH = "face_landmarker.task"

EYE_DOWN_THRESHOLD = 0.015       # Smaller = stricter
EYES_DOWN_TIME_REQUIRED = 10.0   # SECONDS (your requirement)
COOLDOWN_SECONDS = 5             # Prevent spam

# =========================
# LOAD MODEL
# =========================
if not os.path.exists(MODEL_PATH):
    print("❌ face_landmarker.task not found")
    print("Download it from:")
    print("https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task")
    exit(1)

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    num_faces=1
)

landmarker = vision.FaceLandmarker.create_from_options(options)

# =========================
# VIDEO PLAYER (WINDOWS)
# =========================
last_trigger_time = 0

def play_video():
    global last_trigger_time
    now = time.time()

    if now - last_trigger_time < COOLDOWN_SECONDS:
        return

    if os.path.exists(VIDEO_PATH):
        print("💀 DOOMSCROLL CONFIRMED — PLAYING SKELETON 💀")
        os.startfile(VIDEO_PATH)   # Windows native player
        last_trigger_time = now
    else:
        print("❌ Video not found:", VIDEO_PATH)

# =========================
# CAMERA
# =========================
cap = cv2.VideoCapture(0)

eyes_down_start_time = None

print("EYE-ONLY doomscroll detector running")
print("Look DOWN with your EYES for 10 seconds to trigger")
print("Press Q to quit")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    now = time.time()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    result = landmarker.detect(mp_image)

    if result.face_landmarks:
        landmarks = result.face_landmarks[0]

        # LEFT EYE landmarks (stable + reliable)
        upper_eye = landmarks[159].y
        lower_eye = landmarks[145].y

        eye_openness = lower_eye - upper_eye

        if eye_openness < EYE_DOWN_THRESHOLD:
            if eyes_down_start_time is None:
                eyes_down_start_time = now
            else:
                elapsed = now - eyes_down_start_time

                if elapsed >= EYES_DOWN_TIME_REQUIRED:
                    play_video()
                    eyes_down_start_time = None
        else:
            eyes_down_start_time = None

        # Debug overlay
        timer_text = "Eyes up"
        if eyes_down_start_time:
            timer_text = f"Eyes down: {now - eyes_down_start_time:.1f}s"

        cv2.putText(
            frame,
            timer_text,
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )

    cv2.imshow("Doomscroll Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
