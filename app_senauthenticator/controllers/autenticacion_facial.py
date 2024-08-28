from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2
import numpy as np
from app_senauthenticator.serializers.autenticacion_facial import FaceLoginSerializer
from app_senauthenticator.utils.face_utils import convert_to_ndarray, image_to_base64, deserialize_image, read_face_database
from app_senauthenticator.reconocimiento_facial.process.database.config import DataBasePaths
from PIL import Image


class AutenticacionFacial(APIView):
    def __init__(self):
        # self.database_path = "process/database/faces" 
        self.database = DataBasePaths()

    def post(self, request):
        # Verificar si 'face_login' es un archivo
        face_login_file = request.FILES.get('face_login')

        if face_login_file:
            # Convertir el archivo a ndarray directamente
            face_login_ndarray = convert_to_ndarray(face_login_file)

            # Convertir la imagen ndarray a base64 para la validación del serializer
            face_login_data = image_to_base64(Image.fromarray(cv2.cvtColor(face_login_ndarray, cv2.COLOR_BGR2RGB)))

            # Reemplazar 'face_login' en los datos del request
            request.data['face_login'] = face_login_data

        serializer = FaceLoginSerializer(data=request.data)
        if serializer.is_valid():
            face_login_data = serializer.validated_data['face_login']

            try:
                # Paso 1: Deserializar la imagen
                face_login_image = deserialize_image(face_login_data)

                # Paso 2: Leer base de datos de rostros
                face_db, name_db, info = read_face_database(self.face_utils.database.faces)

                if len(face_db) == 0:
                    return Response({"matching": False, "message": "La base de datos está vacía"}, status=status.HTTP_200_OK)

                # Paso 3: Comparar el rostro actual con la base de datos
                matching, user_name = self.face_utils.face_matching(face_login_image, face_db, name_db)

                if matching:
                    return Response({"matching": True, "user_name": user_name}, status=status.HTTP_200_OK)
                else:
                    return Response({"matching": False, "message": "Usuario no encontrado"}, status=status.HTTP_200_OK)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
