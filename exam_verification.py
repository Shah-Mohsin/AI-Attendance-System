import cv2
import face_recognition
import pickle
import time

print("Exam Verification Mode Started")
print("Press Q to quit")

# Load trained model
with open("models/face_encodings.pkl", "rb") as f:
    data = pickle.load(f)

# Safe camera open
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera failed to open")
    exit()

time.sleep(1)

while True:

    ret, frame = cap.read()

    if not ret:
        continue

    # Resize for stability
    small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

    rgb = small[:, :, ::-1]

    # Detect faces
    faces = face_recognition.face_locations(rgb)

    if len(faces) > 0:

        encodings = face_recognition.face_encodings(
            rgb,
            faces
        )

        for encoding in encodings:

            matches = face_recognition.compare_faces(
                data["encodings"],
                encoding,
                tolerance=0.5
            )

            if True in matches:

                index = matches.index(True)

                name = data["names"][index]

                print("Verified:", name)

                cv2.putText(
                    frame,
                    "Verified: " + name,
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )

    cv2.imshow(
        "Exam Verification",
        frame
    )

    key = cv2.waitKey(1)

    if key & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("Verification Ended")