from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import numpy as np
import os
from app_senauthenticator.serializers.inicio_sesion_facial import InicioSesionSerializer
from app_senauthenticator.utils.face_utils import convert_to_ndarray, read_face_database, face_matching


class InicioSesionFacial(APIView):
    def post(self, request):
        serializer = InicioSesionSerializer(data=request.data)
        if serializer.is_valid():
            face_login_file = serializer.validated_data['face_login']

            try:
                # Paso 1: Convertir el archivo de imagen de inicio de sesión a ndarray
                face_login_ndarray = convert_to_ndarray(face_login_file)

                # Obtener el directorio donde están ubicados los archivos de matriz de rostros
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                database_path = os.path.join(base_dir, 'database', 'matrices')

                # Paso 2: Leer base de datos de rostros desde archivos .npy
                face_db, name_db, info = read_face_database(database_path)

                if len(face_db) == 0:
                    return Response({"matching": False, "message": "La base de datos está vacía"}, status=status.HTTP_200_OK)

                # Paso 3: Comparar el rostro actual con la base de datos
                matching, user_name = face_matching(face_login_ndarray, face_db, name_db)

                if matching:
                    return Response({"matching": True, "user_name": user_name}, status=status.HTTP_200_OK)
                else:
                    return Response({"matching": False, "message": "Usuario no encontrado"}, status=status.HTTP_200_OK)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
