from app_senauthenticator.models import Usuario,PasswordReset
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status

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