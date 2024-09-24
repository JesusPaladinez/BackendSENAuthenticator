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



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def usuario_controlador(request, pk=None):
    # Si existe la pk se manejan los métodos GET, PUT, DELETE
    if pk:
        try:
            usuario = Usuario.objects.get(pk=pk)  # Se intenta obtener el objeto por su pk
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)  # Si el objeto no existe
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Otro error

        # Solicitud para obtener un objeto
        if request.method == 'GET':
            try:
                serializer = UsuarioSerializer(usuario)  # Serializar el objeto
                return Response(serializer.data)  # Devolver el objeto serializado
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Solicitud para actualizar un objeto
        if request.method == 'PUT':
            try:
                serializer = UsuarioSerializer(usuario, data=request.data)  # Serializar los datos actualizados
                if serializer.is_valid():
                    serializer.save()  # Guardar los datos actualizados
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Solicitud para eliminar un objeto
        if request.method == 'DELETE':
            try:
                usuario.delete()  # Eliminar el objeto
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Si no existe la pk se manejan los métodos GET, POST
    else:
        # Solicitud para obtener todos los objetos
        if request.method == 'GET':
            try:
                usuarios = Usuario.objects.all()  # Obtener todos los objetos
                serializer = UsuarioSerializer(usuarios, many=True)  # Serializar múltiples objetos
                return Response(serializer.data)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Solicitud para crear un nuevo objeto
        elif request.method == 'POST':
            try:
                usuario_serializer = UsuarioSerializer(data=request.data)
                if usuario_serializer.is_valid():
                    # Guardar el usuario
                    usuario = usuario_serializer.save()
                    usuario.set_password(request.data['password'])  # Encriptar la contraseña
                    usuario.save()

                    # Generar los tokens JWT
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
                        face_register = request.data['face_register']
                        nombre_completo = usuario_serializer.validated_data.get('first_name') + " " + usuario_serializer.validated_data.get('last_name')
                        # numero_documento = usuario_serializer.validated_data.get('numero_documento_usuario')                        

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
                            face_filename = f"{nombre_completo}.png"
                            face_path = os.path.join(face_directory, face_filename)
                            cv2.imwrite(face_path, cropped_face)

                            # Guardar la imagen en formato ndarray en la carpeta 'matrices'
                            matrices_directory = os.path.join(BASE_DIR, 'database', 'matrices')
                            os.makedirs(matrices_directory, exist_ok=True)
                            matrix_filename = f"{nombre_completo}.npy"
                            matrix_path = os.path.join(matrices_directory, matrix_filename)
                            np.save(matrix_path, face_ndarray)

                        except Exception as e:
                            print(f"Error al registrar el rostro: {str(e)}")
                            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                    return response
                else:
                    return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ////////////////////////////////////////////////////////////////
@api_view(['POST'])
def inicio_sesion(request):
    try:        
        user = Usuario.objects.get(numero_documento_usuario=request.data['numero_documento_usuario']) # Obtener el usuario por documento
        
        # Verificar la contraseña
        if not user.check_password(request.data['password']):
            return Response({'error': 'Usuario o Contraseña no son correctos, vuelva a intentar.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generar los tokens JWT (access y refresh)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        # refresh_token = str(refresh)

        serializer = UsuarioSerializer(instance=user)
        response = Response({'user': serializer.data, 'token':access_token}, status=status.HTTP_200_OK)

        # Guardar los tokens en las cookies
        response.set_cookie(
            key='jwt-access',
            value=access_token,
            httponly=True, # Cuando httponly está configurado como true, significa que la cookie solo puede ser accedida por el navegador y no por scripts del lado del cliente (como JavaScript).
            secure= True,  # Cambiar a True en producción
            samesite='None', # Debes usar Secure=True si configuras SameSite='None'.
        
            
        )
        # response.set_cookie(
        #     key='jwt-refresh',
        #     value=refresh_token,
        #     httponly=True,
        #     secure= settings.USE_HTTPS,  # Cambiar a True en producción
        #     samesite='Lax' # (Lax): La cookie se enviará en solicitudes del mismo sitio y en algunas solicitudes de terceros sitios, como las que provienen de enlaces.
        # )

        return response

    except Usuario.DoesNotExist:
        return Response({'error': 'Debe registrarse.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# ////////// fucion protegida que recibe el token y lo valida

@api_view(['GET'])
@permission_classes([IsAuthenticated])  #Extrae y verifica el token enviado en la cabecera Authorization es valido.
def validarToken(request):
    return Response({'message': 'Usuario autenticado correctamente'}, status=200)