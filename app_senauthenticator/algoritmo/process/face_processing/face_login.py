import numpy as np

from process.face_processing.face_utils import FaceUtils
from process.database.config import DataBasePaths


class FaceLogIn:
    def __init__(self):
        self.face_utilities = FaceUtils()
        self.database = DataBasePaths()

        self.matcher = None
        self.comparison = False
        self.cont_frame = 0

    def process(self, face_image: np.ndarray):
        try:
            # Paso 1: Comprobar el rostro detectado
            check_face_detect, face_info, face_save = self.face_utilities.check_face(face_image)
            if check_face_detect is False:
                return face_image, self.matcher, '¡No face detected!'

            # Paso 2: Malla facial
            check_face_mesh, face_mesh_info = self.face_utilities.face_mesh(face_image)
            if check_face_mesh is False:
                return face_image, self.matcher, '¡No face mesh detected!'

            # Paso 3: Extraer malla facial
            face_mesh_points_list = self.face_utilities.extract_face_mesh(face_image, face_mesh_info)

            # Paso 4: Comprobar que el rostro este centrado
            check_face_center = self.face_utilities.check_face_center(face_mesh_points_list)

            # Paso 5: Mostrar estado
            self.face_utilities.show_state_login(face_image, state=self.matcher)

            if check_face_center:
                # Paso 6: Extraer información del rostro
                # bbox & key_points
                self.cont_frame = self.cont_frame + 1
                if self.cont_frame == 48:
                    face_bbox = self.face_utilities.extract_face_bbox(face_image, face_info)
                    face_points = self.face_utilities.extract_face_points(face_image, face_info)

                    # Paso 7: Recortar rostro
                    face_crop = self.face_utilities.face_crop(face_save, face_bbox)

                    # Paso 8: Leer base de datos
                    faces_database, names_database, info = self.face_utilities.read_face_database(self.database.faces)

                    if len(faces_database) != 0 and not self.comparison and self.matcher is None:
                        self.comparison = True
                        # Paso 9: Comparar rostros
                        self.matcher, user_name = self.face_utilities.face_matching(face_crop, faces_database, names_database)

                        if self.matcher:
                            # Paso 10: Guardar los datos y el tiempo
                            self.face_utilities.user_check_in(user_name, self.database.users)
                            return face_image, self.matcher, '¡Usuario autorizado!'
                        else:
                            return face_image, self.matcher, '¡Usuario no autorizado!'
                    else:
                        return face_image, self.matcher, '¡La base de datos está vacía!'
                else:
                    return face_image, self.matcher, 'Esperando cuadros suficientes...'
            else:   
                return face_image, self.matcher, '¡El rostro no está centrado!'
        except Exception as e:
            return face_image, self.matcher, f"Error en la verificación facial: {e}"
