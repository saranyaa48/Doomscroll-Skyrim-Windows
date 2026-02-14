# Doomscroll Skyrim Edition (Windows)

**A computer-vision productivity tool that detects doomscrolling using eye tracking and interrupts it with the Skyrim Skeleton.**

---

## Overview

**Doomscroll Skyrim Edition** is a Windows-based computer vision project that uses your webcam to track **eye movement in real time**.  
If the system detects that you are looking down continuously (a common doomscrolling behavior), it interrupts you by **playing the Skyrim Skeleton video**.

The detection is **eye-only** (not head pose), and includes a **10-second confirmation timer** to prevent false triggers from blinking or brief glances.

---

## How It Works

1. Captures webcam frames using **OpenCV**
2. Uses **MediaPipe Face Landmarker (Tasks API)** to extract eye landmarks
3. Measures downward eye movement (eye openness)
4. Starts a timer when eyes are continuously down
5. If eyes remain down for **10 seconds**:
   - 💀 The Skyrim Skeleton video is launched using the **Windows default video player**

Using the system video player avoids OpenCV video codec issues and ensures reliable playback.

---

## System Requirements

- **Operating System**
  - Windows 10 / 11
- **Python**
  - Version **3.9 – 3.12**
  - ❌ Not compatible with Python 3.13
- **Hardware**
  - Webcam required
- **Permissions**
  - Camera access must be enabled for the terminal / VS Code

---

## Project Structure

DOOMSCROLL-SKYRIM-EDITION/
│
├─ assets/
│ └─ skyrim-skeleton.mp4
│
├─ venv311/ (virtual environment, ignored by git)
│
├─ .gitignore
├─ face_landmarker.task
├─ README.md
├─ requirements.txt
└─ windows_main.py

Create and activate virtual environment (Python 3.11 recommended)
py -3.11 -m venv venv311
venv311\Scripts\activate

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/doomscroll-skyrim-edition.git
cd doomscroll-skyrim-edition

2. Verify:

python --version

3. Install dependencies
pip install -r requirements.txt

4. Download MediaPipe model

Download the Face Landmarker model:

🔗 https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task

Place it in the project root:

face_landmarker.task

5. Add the video asset

Place the video file here:

assets/skyrim-skeleton.mp4

Running the Program
python windows_main.py

Controls

Look down with your eyes for 10 seconds → triggers the video

Press Q → quit the program

Configuration

You can adjust detection behavior directly in windows_main.py.

EYE_DOWN_THRESHOLD

Controls how sensitive the system is to downward eye movement.

EYE_DOWN_THRESHOLD = 0.015


Lower value → stricter detection

Higher value → more sensitive detection

EYES_DOWN_TIME_REQUIRED

How long eyes must remain down before triggering.

EYES_DOWN_TIME_REQUIRED = 10.0

COOLDOWN_SECONDS

Minimum time between video triggers.

COOLDOWN_SECONDS = 5

Limitations

Designed specifically for doomscroll detection

Not suitable for:

Reading books

Writing

Offline desk work

Requires good lighting and a clear view of the eyes

Detection accuracy depends on camera quality

Why Windows Default Video Player?

The video is launched using:

os.startfile("assets/skyrim-skeleton.mp4")


This avoids:

OpenCV video decoding issues
Black screen playback
Codec incompatibilities