from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app_senauthenticator.models import Usuario
from app_senauthenticator.serializers.usuario import UsuarioSerializer
import numpy as np
# import os
import cv2
from app_senauthenticator.serializers.inicio_sesion_facial import InicioSesionSerializer
from app_senauthenticator.utils.face_utils import convert_to_ndarray, read_face_database, face_matching


# class InicioSesionFacial(APIView):
#     def post(self, request):
#         serializer = InicioSesionSerializer(data=request.data)
#         if serializer.is_valid():
#             face_login_file = serializer.validated_data['face_login']

#             try:
#                 # Paso 1: Convertir el archivo de imagen de inicio de sesión a ndarray
#                 face_login_ndarray = convert_to_ndarray(face_login_file)

#                 # Obtener el directorio donde están ubicados los archivos de matriz de rostros
#                 base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#                 database_path = os.path.join(base_dir, 'database', 'matrices')

#                 # Paso 2: Leer base de datos de rostros desde archivos .npy
#                 face_db, name_db, info = read_face_database(database_path)

#                 if len(face_db) == 0:
#                     return Response({"matching": False, "message": "La base de datos está vacía"}, status=status.HTTP_200_OK)

#                 # Paso 3: Comparar el rostro actual con la base de datos
#                 matching, user_name = face_matching(face_login_ndarray, face_db, name_db)

#                 if matching:
#                     return Response({"matching": True, "user_name": user_name}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({"matching": False, "message": "Usuario no encontrado"}, status=status.HTTP_200_OK)

#             except ValueError as e:
#                 return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#             except Exception as e:
#                 return Response({"error": f'Error al iniciar sesión: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# import os
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# class InicioSesionFacial(APIView):
#     def post(self, request):
#         serializer = InicioSesionSerializer(data=request.data)
#         if serializer.is_valid():
#             face_login_file = serializer.validated_data['face_login']

#             try:
#                 # Paso 1: Convertir el archivo de imagen de inicio de sesión a ndarray
#                 face_login_ndarray = convert_to_ndarray(face_login_file)
#                 print("Imagen convertida a ndarray correctamente.")

#                 # Obtener el directorio donde están ubicados los archivos de matriz de rostros
#                 base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#                 database_path = os.path.join(base_dir, 'database', 'matrices')

#                 # Paso 2: Leer base de datos de rostros desde archivos .npy
#                 face_db, name_db, info = read_face_database(database_path)
#                 print("Base de datos de rostros leída correctamente.")

#                 if len(face_db) == 0:
#                     print("La base de datos de rostros está vacía.")
#                     return Response({"error": "No hay rostros en la base de datos."}, status=status.HTTP_404_NOT_FOUND)

#                 # Aquí debería ir el código para recorrer la base de datos y comparar los rostros
#                 for i, face in enumerate(face_db):
#                     # Comparar face_login_ndarray con cada face en face_db
#                     print(f"Comparando con rostro {i} en la base de datos.")
#                     # Lógica de comparación aquí

#                 return Response({"success": "Proceso de inicio de sesión completado."}, status=status.HTTP_200_OK)

#             except Exception as e:
#                 print(f"Error durante el proceso de inicio de sesión: {e}")
#                 return Response({"error": "Error durante el proceso de inicio de sesión."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             print("Datos de entrada no válidos.")
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# import os
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# class InicioSesionFacial(APIView):
#     def post(self, request):
#         serializer = InicioSesionSerializer(data=request.data)
#         if serializer.is_valid():
#             face_login_file = serializer.validated_data['face_login']

#             try:
#                 # Paso 1: Convertir el archivo de imagen de inicio de sesión a ndarray
#                 face_login_ndarray = convert_to_ndarray(face_login_file)
#                 print("Imagen convertida a ndarray correctamente.")

#                 # Obtener el directorio donde están ubicados los archivos de matriz de rostros
#                 base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#                 database_path = os.path.join(base_dir, 'database', 'matrices')

#                 # Paso 2: Leer base de datos de rostros desde archivos .npy
#                 face_db, name_db, info = read_face_database(database_path)
#                 print("Base de datos de rostros leída correctamente.")

# if len(face_db) == 0:
#     print("La base de datos de rostros está vacía.")
#     return Response({"error": "No hay rostros en la base de datos."}, status=status.HTTP_404_NOT_FOUND)

# # Aquí debería ir el código para recorrer la base de datos y comparar los rostros
# for i, face in enumerate(face_db):
#     # Comparar face_login_ndarray con cada face en face_db
#     print(f"Comparando con rostro {i} en la base de datos.")
#     # Lógica de comparación aquí
#     if compare_faces(face_login_ndarray, face):
#         # Si hay una coincidencia, obtener el ID del usuario correspondiente
#         usuario_id = info[i]['id']  # Suponiendo que 'info' contiene un diccionario con los IDs de los usuarios
#         print(f"Usuario autenticado con ID: {usuario_id}")

#         # Recuperar los datos del usuario desde la base de datos usando el ID
#         usuario = Usuario.objects.get(id=usuario_id)
#         usuario_serializer = UsuarioSerializer(usuario)

#         # Retornar los datos del usuario
#         return Response(usuario_serializer.data, status=status.HTTP_200_OK)

# # Si no se encuentra ninguna coincidencia
# return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

# except Exception as e:
#     print(f"Error durante el proceso de inicio de sesión: {e}")
#     return Response({"error": "Error durante el proceso de inicio de sesión."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# else:
#     print("Datos de entrada no válidos.")
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os

class InicioSesionFacial(APIView):
    def post(self, request):
        serializer = InicioSesionSerializer(data=request.data)
        if serializer.is_valid():
            face_login_file = serializer.validated_data['face_login']

            try:
                # Paso 1: Convertir el archivo de imagen de inicio de sesión a ndarray
                face_login_ndarray = convert_to_ndarray(face_login_file)
                print("Imagen convertida a ndarray correctamente.")

                # Convertir la imagen a formato BGR
                face_bgr = cv2.cvtColor(face_login_ndarray, cv2.COLOR_RGB2BGR)

                # Obtener el directorio donde están ubicados los archivos de matriz de rostros
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                database_path = os.path.join(base_dir, 'database', 'matrices')

                # Paso 2: Leer base de datos de rostros desde archivos .npy
                face_db, name_db, info = read_face_database(database_path)
                print("Base de datos de rostros leída correctamente.")

                if len(face_db) == 0:
                    print("La base de datos de rostros está vacía.")
                    return Response({"error": "No hay rostros en la base de datos."}, status=status.HTTP_404_NOT_FOUND)

                # Aquí debería ir el código para recorrer la base de datos y comparar los rostros
                for i, face in enumerate(face_db):
                    # Comparar face_login_ndarray con cada face en face_db
                    print(f"Comparando con rostro {i} en la base de datos.")
                    # Lógica de comparación aquí
                    if face_matching(face_bgr, face):
                        # Si hay una coincidencia, obtener el ID del usuario correspondiente
                        usuario_id = info[i]['id']  # Suponiendo que 'info' contiene un diccionario con los IDs de los usuarios
                        print(f"Usuario autenticado con ID: {usuario_id}")

                        # Recuperar los datos del usuario desde la base de datos usando el ID
                        usuario = Usuario.objects.get(id=usuario_id)
                        usuario_serializer = UsuarioSerializer(usuario)

                        # Retornar los datos del usuario
                        return Response(usuario_serializer.data, status=status.HTTP_200_OK)

                # Si no se encuentra ninguna coincidencia
                return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                print(f"Error durante el proceso de inicio de sesión: {e}")
                return Response({"error": "Error durante el proceso de inicio de sesión."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Datos de entrada no válidos.")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)