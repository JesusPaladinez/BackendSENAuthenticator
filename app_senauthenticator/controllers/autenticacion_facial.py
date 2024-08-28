from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2
import numpy as np
from app_senauthenticator.serializers.inicio_sesion_facial import InicioSesionSerializer
from app_senauthenticator.serializers.registro_facial import RegistroFacialSerializer
from app_senauthenticator.utils.face_utils import convert_to_ndarray, image_to_base64, deserialize_image, read_face_database, face_matching
from app_senauthenticator.reconocimiento_facial.process.database.config import DataBasePaths
from PIL import Image
import os


class InicioSesionFacial(APIView):
    def post(request):
        serializer = InicioSesionSerializer(data=request.data)
        if serializer.is_valid():
            
            # Verificar si 'face_login' es un archivo
            face_login_file = serializer.validated_data['face_login']

            if face_login_file:
                # Convertir el archivo a ndarray directamente
                face_login_ndarray = convert_to_ndarray(face_login_file)

                # Convertir la imagen ndarray a base64 para la validación del serializer
                face_login_data = image_to_base64(Image.fromarray(cv2.cvtColor(face_login_ndarray, cv2.COLOR_BGR2RGB)))

                # Reemplazar 'face_login' en los datos del request
                request.data['face_login'] = face_login_data
            # else:
            #     print('No reconoce la imagen')
            #     face_login_data = serializer.validated_data['face_login']

            try:
                # Paso 1: Deserializar la imagen
                face_login_image = deserialize_image(face_login_data)

                database_path = 'app_senauthenticator/reconocimiento_facial/process/database/faces'
                # Paso 2: Leer base de datos de rostros
                face_db, name_db, info = read_face_database(database_path)

                if len(face_db) == 0:
                    return Response({"matching": False, "message": "La base de datos está vacía"}, status=status.HTTP_200_OK)

                # Paso 3: Comparar el rostro actual con la base de datos
                matching, user_name = face_matching(face_login_image, face_db, name_db)

                if matching:
                    return Response({"matching": True, "user_name": user_name}, status=status.HTTP_200_OK)
                else:
                    return Response({"matching": False, "message": "Usuario no encontrado"}, status=status.HTTP_200_OK)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistroFacial(APIView):
    def post(self, request):
        # Usar el serializer para validar los datos
        serializer = RegistroFacialSerializer(data=request.data)
        if serializer.is_valid():
            face_register = serializer.validated_data['face_register'] # Verificar si 'face_register' es un archivo
            numero_documento = serializer.validated_data.get('numero_documento')

            try:
                # Convertir la imagen a ndarray
                face_ndarray = convert_to_ndarray(face_register)

                # Definir la ruta donde se guardará la imagen
                face_directory = os.path.join('database', 'faces')
                os.makedirs(face_directory, exist_ok=True)

                face_filename = f"{numero_documento}.png"
                face_path = os.path.join(face_directory, face_filename)

                # Guardar la imagen en formato PNG
                cv2.imwrite(face_path, face_ndarray)

                return Response({"success": True, "message": f"Rostro registrado con éxito en {face_path}."}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Si los datos no son válidos, devolver errores de validación
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
