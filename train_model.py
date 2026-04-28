import face_recognition
import os
import pickle

dataset_path = "dataset"

encodings = []
names = []

print("Training started...")

for person in os.listdir(dataset_path):

    person_folder = os.path.join(
        dataset_path,
        person
    )

    for image_name in os.listdir(
        person_folder
    ):

        image_path = os.path.join(
            person_folder,
            image_name
        )

        print("Processing:", image_path)

        image = face_recognition.load_image_file(
            image_path
        )

        faces = face_recognition.face_locations(
            image
        )

        if len(faces) > 0:

            encoding = face_recognition.face_encodings(
                image
            )[0]

            encodings.append(encoding)

            names.append(person)

data = {
    "encodings": encodings,
    "names": names
}

os.makedirs("models", exist_ok=True)

with open(
    "models/face_encodings.pkl",
    "wb"
) as file:

    pickle.dump(data, file)

print("Training completed successfully.")