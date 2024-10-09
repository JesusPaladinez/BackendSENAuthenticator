from app_senauthenticator.models import Usuario,PasswordReset
from django.shortcuts import  redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from rest_framework.views import APIView
from app_senauthenticator.serializers.recuperar_contraseña import PasswordResetSerializer
from rest_framework.response import Response

class ForgotPassword(APIView):
    @csrf_exempt
    def post(self, request):
        email = request.data.get('email')

        try:
            user = Usuario.objects.get(email=email)

            new_password_reset = PasswordReset(usuario=user)
            new_password_reset.save()


            full_password_reset_url = request.build_absolute_uri(reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id}))
            context = {
                'full_password_reset_url': full_password_reset_url,
                'email': email
            }

            html_message = render_to_string("email.html", context=context)
            plain_message = strip_tags(html_message)

            email_message = EmailMultiAlternatives(
                'Resete tu contraseña',  # email subject
                plain_message,
                settings.EMAIL_HOST_USER,  # email sender
                [email]  # email receiver
            )
            

        
            email_message.attach_alternative(html_message, "text/html")
            email_message.fail_silently = True
            email_message.send()

       
            # return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)
            # return Response('password-reset-sent', reset_id=new_password_reset.reset_id)
            return Response({'message': 'password-reset-sent'}, status=302, headers={'Location': reverse('password-reset-sent', args=[new_password_reset.reset_id])})

        except Usuario.DoesNotExist:
            
            # return redirect('forgot-password',{'error': f"Ningun usuario con este correo '{email}' encontrado"}, status=status.HTTP_404_NOT_FOUND)
            return Response('forgot-password',{'error': f"Ningun usuario con este correo '{email}' encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
class PasswordResetSent(APIView):
    def get(self, request, reset_id):
        if PasswordReset.objects.filter(reset_id=reset_id).exists():
            return Response({'message': 'Correo electrónico de restablecimiento de contraseña enviado'},status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid reset id'}, status=status.HTTP_400_BAD_REQUEST)
        


class ResetPassword(APIView):
    @csrf_exempt
    def post(self, request, reset_id):
        try:
            password_reset_id = PasswordReset.objects.get(reset_id=reset_id)
            password = request.data.get('password')
            confirm_password = request.data.get('confirm_password')
            passwords_have_error = False
                
                
            if password != confirm_password:
                passwords_have_error = True
                return JsonResponse({'message': 'Contraseñas no coinciden'}, status=status.HTTP_400_BAD_REQUEST)
                

            if len(password) < 8:
                passwords_have_error = True
                return JsonResponse({'message': 'La contraseña debe ser mayor a 8 digitos'}, status=status.HTTP_400_BAD_REQUEST)
                

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                password_reset_id.delete()
                return JsonResponse(request,{'message': 'El link ha expirado'}, status=status.HTTP_408_REQUEST_TIMEOUT)
                
                

            if not passwords_have_error:
                user = password_reset_id.usuario
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                
                
                return JsonResponse({'message': 'Contraseña reseteada. Procede a loguearte'}, status=status.HTTP_200_OK)
            else:
                
                # return redirect('reset-password', reset_id=reset_id)
                return Response('reset-password', reset_id=reset_id)
                

        except PasswordReset.DoesNotExist:
            return JsonResponse(request,{'message': 'Invalido reseteo id'}, status=status.HTTP_304_NOT_MODIFIED)
            
       

# @csrf_exempt
# def ForgotPassword(request):
#     if request.method == "POST":
#         email = request.POST.get('email')

#         try:
#             user = Usuario.objects.get(email=email)

#             new_password_reset = PasswordReset(usuario=user)
#             new_password_reset.save()


#             full_password_reset_url = request.build_absolute_uri(reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id}))
#             context = {
#                 'full_password_reset_url': full_password_reset_url,
#                 'email': email
#             }

#             html_message = render_to_string("email.html", context=context)
#             plain_message = strip_tags(html_message)

#             email_message = EmailMultiAlternatives(
#                 'Resete tu contraseña',  # email subject
#                 plain_message,
#                 settings.EMAIL_HOST_USER,  # email sender
#                 [email]  # email receiver
#             )
            

        
#             email_message.attach_alternative(html_message, "text/html")
#             email_message.fail_silently = True
#             email_message.send()

       
#             return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

#         except Usuario.DoesNotExist:
            
#             return redirect('forgot-password',{'error': f"Ningun usuario con este correo '{email}' encontrado"}, status=status.HTTP_404_NOT_FOUND)




# def PasswordResetSent(request, reset_id):

#     if PasswordReset.objects.filter(reset_id=reset_id).exists():
#         return JsonResponse({'message': 'Password reset sent'})
       
#     else:
        
#         messages.error(request, 'Invalid reset id')
#         return redirect('forgot-password')




        

# @csrf_exempt
# def ResetPassword(request, reset_id):

#     try:
#         password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

#         if request.method == "POST":
#             password = request.POST.get('password')
#             confirm_password = request.POST.get('confirm_password')

#             passwords_have_error = False

#             if password != confirm_password:
#                 passwords_have_error = True
#                 messages.error(request, 'Contraseñas no coinciden')
                

#             if len(password) < 8:
#                 passwords_have_error = True
#                 messages.error(request, 'La contraseña debe ser mator a 8 digitos')
                

#             expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

#             if timezone.now() > expiration_time:
#                 passwords_have_error = True
#                 password_reset_id.delete()
#                 messages.error(request, 'El link ha expirado')
                

#             if not passwords_have_error:
#                 user = password_reset_id.usuario
#                 user.set_password(password)
#                 user.save()

#                 password_reset_id.delete()

#                 messages.success(request, 'Contraseña reseteada. Procede a loguearte')
                
#                 return JsonResponse({'message': 'Contraseña reseteada. Procede a loguearte'}, status=status.HTTP_200_OK)
#             else:
                
#                 return redirect('reset-password', reset_id=reset_id)
                

#     except PasswordReset.DoesNotExist:
#         messages.error(request, 'Invalido reseteo id')
#         return redirect('forgot-password')
        

   