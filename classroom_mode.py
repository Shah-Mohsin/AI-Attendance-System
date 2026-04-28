import cv2
import face_recognition
import pickle
import sqlite3
from datetime import datetime

conn = sqlite3.connect("database/classroom.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS classroom_attendance (
    name TEXT,
    subject TEXT,
    date TEXT,
    time TEXT
)
""")

conn.commit()

subject = input("Enter Subject Name: ")

print("Classroom Mode Started")
print("Press Q to quit")

with open("models/face_encodings.pkl", "rb") as f:
    data = pickle.load(f)

cap = cv2.VideoCapture(0)

marked = set()

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    rgb = frame[:, :, ::-1]

    faces = face_recognition.face_locations(rgb)

    encodings = face_recognition.face_encodings(rgb, faces)

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

                time = now.strftime("%H:%M:%S")

                cursor.execute(
                    "INSERT INTO classroom_attendance VALUES (?,?,?,?)",
                    (name,subject,date,time)
                )

                conn.commit()

                marked.add(name)

                print(name,"marked in",subject)

    cv2.imshow("Smart Classroom Mode", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
conn.close()

print("Classroom session ended.")