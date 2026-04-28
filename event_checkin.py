import cv2
import face_recognition
import pickle
import sqlite3
from datetime import datetime
import time

print("Event Check-in Mode Started")

event_name = input("Enter Event Name: ").strip()

if event_name == "":
    event_name = "Default Event"

print("Press Q to quit")

# =========================
# DATABASE SETUP
# =========================

conn = sqlite3.connect("database/events.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS event_checkin (
    name TEXT,
    event_name TEXT,
    date TEXT,
    time TEXT
)
""")

conn.commit()

# =========================
# LOAD MODEL
# =========================

with open("models/face_encodings.pkl", "rb") as f:
    data = pickle.load(f)

# =========================
# CAMERA
# =========================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera failed to open")
    exit()

time.sleep(1)

marked = set()

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    small = cv2.resize(
        frame,
        (0,0),
        fx=0.5,
        fy=0.5
    )

    rgb = small[:, :, ::-1]

    faces = face_recognition.face_locations(rgb)

    if len(faces) > 0:

        encodings = face_recognition.face_encodings(
            rgb,
            faces
        )

        for encoding in encodings:

            matches = face_recognition.compare_faces(
                data["encodings"],
                encoding
            )

            if True in matches:

                index = matches.index(True)

                name = data["names"][index]

                if name not in marked:

                    now = datetime.now()

                    date = now.strftime("%Y-%m-%d")
                    time_now = now.strftime("%H:%M:%S")

                    cursor.execute(
                        "INSERT INTO event_checkin VALUES (?,?,?,?)",
                        (name,event_name,date,time_now)
                    )

                    conn.commit()

                    marked.add(name)

                    print(name,"checked into",event_name)

    cv2.imshow(
        "Event Check-in Mode",
        frame
    )

    key = cv2.waitKey(1)

    if key & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

conn.close()

print("Event session ended.")