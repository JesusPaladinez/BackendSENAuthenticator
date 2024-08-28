import os
import numpy as np
import cv2
import datetime
from typing import List, Tuple, Any
from ..reconocimiento_facial.process.face_processing.face_matcher import face_matching_face_recognition_model
import base64
from io import BytesIO
from PIL import Image

    
# Convertir el archivo de imagen a base64
def image_to_base64(image) -> str:        
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# Deserializar la imagen desde base64
def deserialize_image(image_data: str) -> np.ndarray:        
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# Convertir la imagen a un formato ndarray
def convert_to_ndarray(image_file) -> np.ndarray:
    image = Image.open(image_file)
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# Guardar rostro
def save_face(self, face_crop: np.ndarray, user_code: str, path: str):
    if len(face_crop) != 0:
        if self.angle is not None and -5 < self.angle < 5:
            face_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
            cv2.imwrite(f"{path}/{user_code}.png", face_crop)
            return True
    else:
        return False


# Leer base de datos
def read_face_database(database_path: str) -> Tuple[List[np.ndarray], List[str], str]:
    face_db: List[np.ndarray] = []
    face_names: List[str] = []

    for file in os.listdir(database_path):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(database_path, file)
            img_read = cv2.imread(img_path)
            if img_read is not None:
                face_db.append(img_read)
                face_names.append(os.path.splitext(file)[0])

    return face_db, face_names, f'Comparando {len(face_db)} rostros!'


def face_matching(current_face: np.ndarray, face_db: List[np.ndarray], name_db: List[str]) -> Tuple[bool, str]:
    user_name: str = ''
    current_face = cv2.cvtColor(current_face, cv2.COLOR_RGB2BGR)
    for idx, face_img in enumerate(face_db):
        matching, distance = face_matching_face_recognition_model(current_face, face_img)
        print(f'Comparando el rostro con el usuario: {name_db[idx]}')
        print(f'matching: {matching} distance: {distance}')
        if matching:
            user_name = name_db[idx]
            return matching, user_name
    return False, 'Rostro desconocido'


def user_check_in(self, user_name: str, user_path: str):
    if not self.user_registered:
        now = datetime.datetime.now()
        date_time = now.strftime("%Y-%m-%d a las %H:%M:%S")
        user_file_path = os.path.join(user_path, f"{user_name}.txt")
        with open(user_file_path, "a")as user_file:
            user_file.write(f'\nAccedió el: {date_time}\n')

        self.user_registered = True