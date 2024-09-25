# Librerías para registrar los datos del usuario
from rest_framework_simplejwt.tokens import RefreshToken  # Importar JWT
from app_senauthenticator.models import Usuario,PasswordReset
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

#  Importaciones Recuperar contraseña
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse



@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def usuario_controlador(request, pk=None):
    try:
        if pk:
            usuario = Usuario.objects.get(pk=pk)

            # Solicitud para obtener un objeto
            if request.method == 'GET':
                serializer = UsuarioSerializer(usuario)
                return Response(serializer.data)

            # Solicitud para actualizar un objeto
            elif request.method == 'PUT':
                serializer = UsuarioSerializer(usuario, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Solicitud para eliminar un objeto
            elif request.method == 'DELETE':
                usuario.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            # Solicitud para obtener todos los objetos
            if request.method == 'GET':
                usuarios = Usuario.objects.all()
                serializer = UsuarioSerializer(usuarios, many=True)
                return Response(serializer.data)

            # Solicitud para crear un nuevo objeto
            elif request.method == 'POST':
                # Extraer el número de documento del request.data
                numero_documento = request.data.get('numero_documento_usuario')

                # Asignar el número de documento al campo username en el request.data
                request.data['username'] = numero_documento

                # Crear un nuevo usuario con los datos actualizados
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
                        return registrar_rostro(request.data['face_register'], usuario_serializer)

                    return response
                return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Error en el controlador de usuario: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


@api_view(['GET']) # Se utiliza el método GET para recibir las credenciales del usuario 
@authentication_classes([TokenAuthentication]) # Se utiliza autenticación por token
@permission_classes([IsAuthenticated]) # Se requiere que el usuario esté autenticado
def perfil(request):
    try:
        serializer = UsuarioSerializer(instance=request.user) # Se serializa los datos del usuario

        # return Response(f'El usuario {serializer.data["first_name"]} {serializer.data["last_name"]} está activo en el sistema.')
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@csrf_exempt
def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = Usuario.objects.get(email=email)

            new_password_reset = PasswordReset(usuario=user)
            new_password_reset.save()

            # password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = request.build_absolute_uri(reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id}))

            email_body = f'Reseta tu contraseña con este link:\n\n\n{full_password_reset_url}'

            email_message = EmailMessage(
                'Resete tu contraseña',  # email subject
                email_body,
                settings.EMAIL_HOST_USER,  # email sender
                [email]  # email receiver
            )

            # print("Email message created:", email_message)
            email_message.fail_silently = True
            email_message.send()
            # print("Email sent successfully!")

            # return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)
            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except Usuario.DoesNotExist:
            # messages.error(request, f"Ningun usuario con este correo '{email}' encontrado")
            # return redirect('forgot-password')
            return redirect('forgot-password',{'error': f"Ningun usuario con este correo '{email}' encontrado"}, status=status.HTTP_404_NOT_FOUND)


    return render(request, 'forgot_password.html')
    # return JsonResponse(request,{'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def PasswordResetSent(request, reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return JsonResponse({'message': 'Password reset sent'})
        # return render(request)
        # return JsonResponse(request,{'message': 'Password reset sent'})
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
        # return Response({'error': 'Invalid reset id'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Contraseñas no coinciden')
                # return JsonResponse({'error': 'Contraseñas no coinciden'}, status=status.HTTP_400_BAD_REQUEST)

            if len(password) < 8:
                passwords_have_error = True
                messages.error(request, 'La contraseña debe ser mator a 8 digitos')
                # return JsonResponse({'error': 'La contraseña debe ser mayor a 8 digitos'}, status=status.HTTP_400_BAD_REQUEST)

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                password_reset_id.delete()
                messages.error(request, 'El link ha expirado')
                # return JsonResponse({'error': 'El link ha expirado'}, status=status.HTTP_410_GONE)

                

            if not passwords_have_error:
                user = password_reset_id.usuario
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Contraseña reseteada. Procede a loguearte')
                # return redirect('login')
                return JsonResponse({'message': 'Contraseña reseteada. Procede a loguearte'}, status=status.HTTP_200_OK)
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)
                # return Response({'error': 'Error al resetear contraseña'}, status=status.HTTP_400_BAD_REQUEST)

    
    except PasswordReset.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalido reseteo id')
        return redirect('forgot-password')
        # return Response({'error': 'Invalido reseteo id'}, status=status.HTTP_404_NOT_FOUND)

    # return render(request, 'reset_password.html')