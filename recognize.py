import cv2
import face_recognition
import pickle
import sqlite3
from datetime import datetime
import numpy as np
import time

print("Loading trained model...")

with open("models/face_encodings.pkl", "rb") as f:
    data = pickle.load(f)

print("Model loaded successfully.")

# ============================
# CREATE DATABASE (CORRECT)
# ============================

conn = sqlite3.connect("database/attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    name TEXT,
    date TEXT,
    time TEXT,
    status TEXT,
    confidence REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS unknown_log (
    date TEXT,
    time TEXT
)
""")

conn.commit()

# ============================
# CAMERA
# ============================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera failed")
    exit()

time.sleep(1)

print("Camera started successfully.")
print("Press Q to quit")

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

        for encoding, face_location in zip(encodings, faces):

            distances = face_recognition.face_distance(
                data["encodings"],
                encoding
            )

            best_match_index = np.argmin(distances)

            confidence = round(
                (1 - distances[best_match_index]) * 100,
                2
            )

            matches = face_recognition.compare_faces(
                data["encodings"],
                encoding
            )

            name = "Unknown"

            if matches[best_match_index]:

                name = data["names"][best_match_index]

                if name not in marked:

                    now = datetime.now()

                    date = now.strftime("%Y-%m-%d")
                    time_now = now.strftime("%H:%M:%S")

                    status = "Present"

                    cursor.execute(
                        "INSERT INTO attendance VALUES (?,?,?,?,?)",
                        (name,date,time_now,status,confidence)
                    )

                    conn.commit()

                    marked.add(name)

                    print(
                        name,
                        "marked Present | Confidence:",
                        confidence
                    )

            else:

                now = datetime.now()

                date = now.strftime("%Y-%m-%d")
                time_now = now.strftime("%H:%M:%S")

                cursor.execute(
                    "INSERT INTO unknown_log VALUES (?,?)",
                    (date,time_now)
                )

                conn.commit()

            # Draw box

            top, right, bottom, left = face_location

            top *= 2
            right *= 2
            bottom *= 2
            left *= 2

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0,255,0),
                2
            )

            label = f"{name} ({confidence}%)"

            cv2.putText(
                frame,
                label,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )

    cv2.imshow(
        "AI Attendance System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

conn.close()

print("Attendance session ended.")