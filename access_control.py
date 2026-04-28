import cv2
import face_recognition
import pickle
import time

print("Access Control Mode Started")
print("Press Q to quit")

authorized_people = [
    "Mohsin",
    "Adnan",
    "Faisal"
]

with open("models/face_encodings.pkl", "rb") as f:
    data = pickle.load(f)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera failed to open")
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

            if True in matches:

                index = matches.index(True)

                name = data["names"][index]

                if name in authorized_people:

                    message = "ACCESS GRANTED"
                    color = (0,255,0)

                else:

                    message = "ACCESS DENIED"
                    color = (0,0,255)

                print(name, message)

                cv2.putText(
                    frame,
                    message,
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    color,
                    2
                )

    cv2.imshow(
        "Access Control",
        frame
    )

    key = cv2.waitKey(1)

    if key & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("Access Control Ended")
