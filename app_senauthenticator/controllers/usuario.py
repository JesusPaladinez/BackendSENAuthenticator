# Librerías para registrar los datos del usuario
from rest_framework_simplejwt.tokens import RefreshToken  # Importar JWT
from app_senauthenticator.models import Usuario
from app_senauthenticator.serializers.usuario import UsuarioSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Librerías para el reconocimiento facial
from app_senauthenticator.utils.face_utils import convert_to_ndarray, detect_face_dlib, crop_face
import os
import cv2
import numpy as np


@api_view(['GET', 'POST'])
def usuarios_controlador(request):
    if request.method == 'GET':
        return obtener_usuarios(request._request)
    elif request.method == 'POST':
        return crear_usuario(request._request)


@api_view(['GET', 'PUT', 'DELETE'])
def usuarios_detalle_controlador(request, pk):
    if request.method == 'GET':
        return obtener_usuario(request._request, pk)
    elif request.method == 'PUT':
        return actualizar_usuario(request._request, pk)
    elif request.method == 'DELETE':
        return eliminar_usuario(request._request, pk)


@api_view(['GET'])
def obtener_usuarios(request):
    try:
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error al obtener los usuarios: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def crear_usuario(request):
    try:
        numero_documento = request.data.get('numero_documento_usuario')
        if not numero_documento:
            return Response({'error': 'El número de documento es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)

        # Asignar el número de documento al campo username
        request.data['username'] = numero_documento

        # Crear un nuevo usuario con los datos actualizados
        usuario_serializer = UsuarioSerializer(data=request.data)
        if usuario_serializer.is_valid():
            usuario = usuario_serializer.save()
            usuario.set_password(request.data['password'])  # Encriptar la contraseña
            usuario.save()

            # Generar tokens JWT
            refresh = RefreshToken.for_user(usuario)
            access_token = str(refresh.access_token)

            # Crear la respuesta con los tokens en cookies
            response = Response({'usuario': usuario_serializer.data}, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='jwt-access',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None'
            )

            # Procesar el registro facial si se proporciona una imagen
            if 'face_register' in request.data:
                return registrar_rostro(request.data['face_register'], usuario_serializer)

            return response
        else:
            return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except KeyError as e:
        return Response({'error': f'Campo faltante: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'Error al crear el usuario: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def registrar_rostro(face_register, usuario_serializer):
    try:
        # Convertir la imagen a ndarray
        face_ndarray = convert_to_ndarray(face_register)

        # Detectar el rostro en la imagen
        face_detected = detect_face_dlib(face_ndarray)
        if face_detected is None:
            raise ValueError("No se detectó ningún rostro en la imagen proporcionada.")

        # Recortar el rostro detectado
        cropped_face = crop_face(face_ndarray, face_detected)

        # Guardar la imagen final en formato PNG
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        face_directory = os.path.join(BASE_DIR, 'database', 'faces')
        os.makedirs(face_directory, exist_ok=True)
        nombre_completo = f"{usuario_serializer.validated_data.get('first_name')} {usuario_serializer.validated_data.get('last_name')}"
        face_filename = f"{nombre_completo}.png"
        face_path = os.path.join(face_directory, face_filename)
        cv2.imwrite(face_path, cropped_face)

        # Guardar la imagen en formato ndarray en la carpeta 'matrices'
        matrices_directory = os.path.join(BASE_DIR, 'database', 'matrices')
        os.makedirs(matrices_directory, exist_ok=True)
        matrix_filename = f"{nombre_completo}.npy"
        matrix_path = os.path.join(matrices_directory, matrix_filename)
        np.save(matrix_path, face_ndarray)

        return Response({"message": "Rostro registrado correctamente."}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Error al registrar el rostro: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def obtener_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def actualizar_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def eliminar_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def inicio_sesion(request):
    try:
        user = Usuario.objects.get(numero_documento_usuario=request.data['numero_documento_usuario'])  # Obtener el usuario por documento

        # Verificar la contraseña
        if not user.check_password(request.data['password']):
            return Response({'error': 'Usuario o contraseña no son correctos, vuelva a intentar.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generar los tokens JWT (access y refresh)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        serializer = UsuarioSerializer(instance=user)
        response = Response({'user': serializer.data, 'token': access_token}, status=status.HTTP_200_OK)

        # Guardar los tokens en las cookies
        response.set_cookie(
            key='jwt-access',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='None',
        )

        return response

    except Usuario.DoesNotExist:
        return Response({'error': 'Debe registrarse.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Error en el inicio de sesión: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Extrae y verifica el token enviado en la cabecera Authorization es válido.
def validarToken(request):
    return Response({'message': 'Usuario autenticado correctamente'}, status=200)


