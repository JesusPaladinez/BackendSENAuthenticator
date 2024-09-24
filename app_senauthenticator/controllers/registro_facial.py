from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2
import numpy as np
from app_senauthenticator.serializers.registro_facial import RegistroFacialSerializer
from app_senauthenticator.utils.face_utils import convert_to_ndarray, detect_face, detect_face_dlib, crop_face
import os


class RegistroFacial(APIView):
    def post(self, request):
        
        # Depurar los datos que llegan
        print(f"Datos recibidos: {request.data}")

        serializer = RegistroFacialSerializer(data=request.data)
        if serializer.is_valid():
            nombre_completo = serializer.validated_data.get('nombre_completo')
            numero_documento = serializer.validated_data.get('numero_documento')
            face_register = serializer.validated_data['face_register']

            try:
                # Paso 1: Convertir la imagen a ndarray
                face_ndarray = convert_to_ndarray(face_register)
                print(f"Imagen convertida a ndarray para documento: {nombre_completo}")
                print(f"Tipo de face_ndarray: {type(face_ndarray)}, Dimensiones: {face_ndarray.shape}")

                # Definir la ruta base y el directorio de las imágenes de rostros
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                face_directory = os.path.join(BASE_DIR, 'database', 'faces')
                os.makedirs(face_directory, exist_ok=True)

                # Paso 2: Detectar el rostro en la imagen
                face_detected = detect_face_dlib(face_ndarray)
                if face_detected is None:
                    raise ValueError("No se detectó ningún rostro en la imagen proporcionada.")
                
                # Paso 3: Recortar el rostro detectado
                cropped_face = crop_face(face_ndarray, face_detected)
                print(f"Rostro detectado y recortado para documento: {nombre_completo}")

                # Paso 4: Guardar la imagen final en formato PNG
                face_filename = f"{nombre_completo}.png"
                face_path = os.path.join(face_directory, face_filename)

                cv2.imwrite(face_path, cropped_face)
                print(f"Imagen guardada en: {face_path}")

                # Paso 5: Guardar la imagen en formato ndarray en la carpeta 'matrices'
                matrices_directory = os.path.join(BASE_DIR, 'database', 'matrices')
                os.makedirs(matrices_directory, exist_ok=True)

                matrix_filename = f"{nombre_completo}.npy"
                matrix_path = os.path.join(matrices_directory, matrix_filename)

                np.save(matrix_path, face_ndarray)
                print(f"Imagen en formato ndarray guardada en: {matrix_path}")

                return Response({
                    "success": True,
                    "message": f"Rostro registrado con éxito en {face_path} y en formato ndarray en {matrix_path}."
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                print(f"Error al registrar el rostro: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
