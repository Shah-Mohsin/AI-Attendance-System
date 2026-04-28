import cv2
import os

name = input("Enter your name: ")

folder = f"dataset/{name}"
os.makedirs(folder, exist_ok=True)

url = "http://10.160.131.69:8080/video"

cap = cv2.VideoCapture(url)

count = 0

print("Press C to capture image")
print("Press Q to quit")

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame not received")
        continue

    cv2.imshow("Phone Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):

        img_path = f"{folder}/{count}.jpg"

        cv2.imwrite(img_path, frame)

        count += 1

        print("Captured:", count)

    elif key == ord('q'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()