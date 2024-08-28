import face_recognition as fr
from deepface import DeepFace
import cv2
import numpy as np
import os
from typing import List, Tuple


class FaceMatcherModel:
    def __init__(self):
        self.model = "DeepID" # Módelo de la librería DeepFace

    def face_matching_face_recognition_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        face_1 = cv2.cvtColor(face_1, cv2.COLOR_BGR2RGB)
        face_2 = cv2.cvtColor(face_2, cv2.COLOR_BGR2RGB)

        face_loc_1 = [(0, face_1.shape[0], face_1.shape[1], 0)]
        face_loc_2 = [(0, face_2.shape[0], face_2.shape[1], 0)]

        face_1_encoding = fr.face_encodings(face_1, known_face_locations=face_loc_1)[0]
        face_2_encoding = fr.face_encodings(face_2, known_face_locations=face_loc_2)

        matching = fr.compare_faces(face_1_encoding, face_2_encoding, tolerance=0.55)
        distance = fr.face_distance(face_1_encoding, face_2_encoding)

        return matching[0], distance[0]

    def face_matching_deepid_model(self, face_1: np.ndarray, face_2: np.ndarray) -> Tuple[bool, float]:
        try:
            result = DeepFace.verify(img1_path=face_1, img2_path=face_2, model_name=self.model)
            matching, distance = result['verified'], result['distance']
            return matching, distance
        except:
            return False, 0.0        


# Metodo find para comparar las imágenes de una db

# class FaceMatcherModel:
#     def __init__(self):
#         self.model = "DeepID" # Módelo de la librería DeepFace
#         self.db_path = "" # Path de la carpeta de la nube en FireBase

#     def prepare_face(self, face: np.ndarray) -> str: # El método recibe la imagen a comparar y devuelve la ruta de la imagen 
#         # Convertir la imagen de BGR a RGB
#         face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
#         # Guardar la imagen temporalmente
#         temp_path = "temp_face.jpg"
#         cv2.imwrite(temp_path, face_rgb)
#         return temp_path

#     def find_similar_faces(self, face: np.ndarray) -> List[Tuple[str, float]]: # El método recibe la imagen a comparar y devuelve una lista con...
#         # Preparar la imagen del rostro
#         temp_face_path = self.prepare_face(face)
        
#         try:
#             # Encontrar rostros similares en la base de datos
#             results = DeepFace.find(img_path=temp_face_path, db_path=self.db_path, model_name=self.model)
#             # Extraer y devolver las rutas de las imágenes y sus distancias
#             similar_faces = [(row['identity'], row['VGG-Face_cosine']) for index, row in results.iterrows()]
#             return similar_faces
#         except Exception as e:
#             print(f"Error en la búsqueda: {e}")
#             return []


# Uso del código probablemente vaya en otro archivo como en process/face_processing/face_utils.py
# Crear el objeto FaceMatcherDeepID especificando la ruta a la carpeta de la base de datos
# matcher = FaceMatcherModel()

# # Leer una imagen de ejemplo
# face_image = cv2.imread("path_to_face_image.jpg")  # Reemplaza con la ruta a tu imagen de rostro

# # Encontrar rostros similares en la base de datos
# similar_faces = matcher.find_similar_faces(face_image)

# # Mostrar los resultados
# for face_path, distance in similar_faces:
#     print(f"Rostro similar encontrado en: {face_path} con una distancia de: {distance}")
