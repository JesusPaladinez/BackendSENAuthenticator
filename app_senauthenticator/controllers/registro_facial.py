from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2
import numpy as np
from app_senauthenticator.serializers.registro_facial import RegistroFacialSerializer
from app_senauthenticator.utils.face_utils import convert_to_ndarray, detect_face, crop_face
import os
import logging


logger = logging.getLogger(__name__)


class RegistroFacial(APIView):
    def post(self, request):
        
        # Depurar los datos que llegan
        logger.info(f"Datos recibidos: {request.data}")

        serializer = RegistroFacialSerializer(data=request.data)
        if serializer.is_valid():
            numero_documento = serializer.validated_data.get('numero_documento')
            face_register = serializer.validated_data['face_register']

            try:
                # Paso 1: Convertir la imagen a ndarray
                face_ndarray = convert_to_ndarray(face_register)
                logger.info(f"Imagen convertida a ndarray para documento: {numero_documento}")

                # Paso 2: Detectar el rostro en la imagen
                face_detected = detect_face(face_ndarray)
                if face_detected is None:
                    raise ValueError("No se detectó ningún rostro en la imagen proporcionada.")
                
                # Paso 3: Recortar el rostro detectado
                cropped_face = crop_face(face_ndarray, face_detected)
                logger.info(f"Rostro detectado y recortado para documento: {numero_documento}")

                # Paso 4: Definir la ruta donde se guardará la imagen PNG
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                face_directory = os.path.join(BASE_DIR, 'database', 'faces')
                os.makedirs(face_directory, exist_ok=True)

                face_filename = f"{numero_documento}.png"
                face_path = os.path.join(face_directory, face_filename)

                # Guardar la imagen en formato PNG
                cv2.imwrite(face_path, cropped_face)
                logger.info(f"Imagen guardada en: {face_path}")

                # Paso 5: Guardar la imagen en formato ndarray en la carpeta 'matrices'
                matrices_directory = os.path.join(BASE_DIR, 'database', 'matrices')
                os.makedirs(matrices_directory, exist_ok=True)

                matrix_filename = f"{numero_documento}.npy"
                matrix_path = os.path.join(matrices_directory, matrix_filename)

                # Guardar el arreglo en formato .npy
                np.save(matrix_path, face_ndarray)
                logger.info(f"Imagen en formato ndarray guardada en: {matrix_path}")

                return Response({
                    "success": True,
                    "message": f"Rostro registrado con éxito en {face_path} y en formato ndarray en {matrix_path}."
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Error al registrar el rostro: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
