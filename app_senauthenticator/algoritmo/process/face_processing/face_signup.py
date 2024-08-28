import numpy as np
from typing import Tuple

from process.face_processing.face_utils import FaceUtils
from process.database.config import DataBasePaths


class FaceSignUp:
    def __init__(self):
        self.database = DataBasePaths()
        self.face_utilities = FaceUtils()

    def process(self, face_image: np.ndarray, user_code: str) -> Tuple[np.ndarray, bool, str]: # La función va a retornar la imagen del rostro, un booleano indicando si se registro y un string con un mensaje para el usuario
        try: 
            # Paso 1: Comprobar el rostro detectado
            check_face_detect, face_info, face_save = self.face_utilities.check_face(face_image)
            if check_face_detect is False:
                return face_image, False, '¡No se ha detectado ningún rostro!'

            # Paso 2: Malla facial
            check_face_mesh, face_mesh_info = self.face_utilities.face_mesh(face_image)
            if check_face_mesh is False:
                return face_image, False, '¡No se ha detectado la malla facial!'

            # Paso 3: Extraer malla facial
            face_mesh_points_list = self.face_utilities.extract_face_mesh(face_image, face_mesh_info)

            # Paso 4: Comprobar que el rostro este centrado
            check_face_center = self.face_utilities.check_face_center(face_mesh_points_list)

            # Paso 5: Mostrar estado
            self.face_utilities.show_state_signup(face_image, state=check_face_center)
            if check_face_center:
                # Paso 6: Extraer información del rostro
                face_bbox = self.face_utilities.extract_face_bbox(face_image, face_info)
                face_points = self.face_utilities.extract_face_points(face_image, face_info)

                # Paso 7: Recortar rostro
                face_crop = self.face_utilities.face_crop(face_save, face_bbox)

                # Paso 8: Guardar rostro
                check_save_image = self.face_utilities.save_face(face_crop, user_code, self.database.faces)
                return face_image, check_save_image, '¡El registro facial ha sido exitoso!'

            else:
                return face_image, False, '¡El rostro no está centrado!'
            
        except Exception as e:
            return face_image, False, f"Error durante el registro facial: {e}"

