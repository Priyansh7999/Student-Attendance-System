#encode.py
from pathlib import Path
import pickle
import face_recognition
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

Path("training").mkdir(exist_ok=True)
Path("output").mkdir(exist_ok=True)

def encode_known_faces(
    model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH
) -> None:
    
    start_time = time.time()
    names = []
    encodings = []
    n = 1

    for filepath in Path("training").glob("*/*"):
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)
        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)
            logging.info(f"{name} done {n}")
            n += 1
    
    name_encodings = {"names": names, "encodings": encodings}
    with encodings_location.open(mode="wb") as f:
        pickle.dump(name_encodings, f)
    end_time = time.time()
    print(f"Total Time Taken: {end_time-start_time:.2f} seconds")
    logging.info(f"Total images encoded: {n-1}")
    return n-1

# encode_known_faces()

# if __name__ == "__main__":
#     start_time = time.time()
#     total_images = encode_known_faces()
#     end_time = time.time()
#     print(f"Total Time Taken: {end_time-start_time:.2f} seconds")
#     print(f"Total Images in Database: {total_images}")
