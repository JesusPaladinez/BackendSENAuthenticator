from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import cv2
import numpy as np
from app_senauthenticator.serializers.rostro import RostroSerializer
from app_senauthenticator.algoritmo.process.face_processing.face_utils import FaceUtils
from PIL import Image
from io import BytesIO
import base64

class FaceVerificationView(APIView):
    def __init__(self):
        self.face_utils = FaceUtils()

    def deserialize_image(self, image_data: str) -> np.ndarray:
        # Deserializar la imagen desde base64
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def post(self, request):
        serializer = RostroSerializer(data=request.data)
        if serializer.is_valid():
            current_face_data = serializer.validated_data['current_face']

            try:
                # Paso 1: Deserializar la imagen
                current_face_image = self.deserialize_image(current_face_data)

                # Paso 2: Leer base de datos de rostros
                face_db, name_db, info = self.face_utils.read_face_database(self.face_utils.database.faces)

                if len(face_db) == 0:
                    return Response({"matching": False, "message": "La base de datos está vacía"}, status=status.HTTP_200_OK)

                # Paso 3: Comparar el rostro actual con la base de datos
                matching, user_name = self.face_utils.face_matching(current_face_image, face_db, name_db)

                if matching:
                    return Response({"matching": True, "user_name": user_name}, status=status.HTTP_200_OK)
                else:
                    return Response({"matching": False, "message": "Usuario no encontrado"}, status=status.HTTP_200_OK)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
