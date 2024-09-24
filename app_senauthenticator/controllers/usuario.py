from rest_framework_simplejwt.tokens import RefreshToken  # Importar JWT
from app_senauthenticator.models import Usuario,PasswordReset
from app_senauthenticator.serializers.usuario import UsuarioSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classesfrom django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import JsonResponse





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
                serializer = UsuarioSerializer(data=request.data)  # Serializar el objeto recibido

                if serializer.is_valid():
                    serializer.save()

                    user = Usuario.objects.get(numero_documento_usuario=serializer.data['numero_documento_usuario'])
                    user.set_password(serializer.data['password'])  # Encriptar la contraseña
                    user.save()

                    # Generar los tokens JWT
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    # refresh_token = str(refresh)

                    # Crear la respuesta con los tokens en cookies
                    response = Response({'usuario': serializer.data}, status=status.HTTP_201_CREATED)

                    # Guardar los tokens en las cookies
                    response.set_cookie(
                        key='jwt-access',
                        value= access_token,
                        httponly=True,
                        secure= True,  # Cambiar a True en producción(https)y false para desarrollo(http)
                        samesite='None'  # Cambiar según configuración de dominio
                    )

                    return response

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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