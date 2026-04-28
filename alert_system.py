import cv2
import face_recognition
import pickle
import sqlite3
from datetime import datetime
import time

print("AI Alert System Started")
print("Press Q to quit")

# =========================
# DATABASE
# =========================

conn = sqlite3.connect("database/attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS unknown_log (
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

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera failed")
    exit()

time.sleep(1)

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

            if True not in matches:

                now = datetime.now()

                date = now.strftime("%Y-%m-%d")
                time_now = now.strftime("%H:%M:%S")

                cursor.execute(
                    "INSERT INTO unknown_log VALUES (?,?)",
                    (date,time_now)
                )

                conn.commit()

                print("⚠ Unknown Person Detected")

                cv2.putText(
                    frame,
                    "UNKNOWN ALERT",
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    2
                )

    cv2.imshow(
        "Alert System",
        frame
    )

    key = cv2.waitKey(1)

    if key & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

conn.close()

print("Alert session ended.")