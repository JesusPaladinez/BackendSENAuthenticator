# import pytest
# from rest_framework.test import APIClient
# from app_senauthenticator.models import Usuario

# from django.urls import reverse
# from rest_framework_simplejwt.tokens import RefreshToken

# @pytest.mark.django_db
# def test_crear_usuario():
#     client = APIClient()
#     data = {
#             "last_name": "Castañeda",
#             "email": "moto.emacasta12@gmail.com",
#             "tipo_documento_usuario": "Cedula de ciudadania",
#             "genero_usuario": "Masculino",
#             "rol_usuario": "Administrador",
#             "numero_documento_usuario": 101010,
#             "password": "1234",
#             "username": "emmanuel_casta"
#     }

#     response = client.post(reverse('cont_usuario'), data, format='json')
#     print(response.data)  

#     assert response.status_code == 201
#     # assert response.status_code == 400 si esta mal algo
    
#     # assert Usuario.objects.filter(numero_documento_usuario='12345678').exists()

# @pytest.mark.django_db
# def test_obtener_usuarios():
#     client = APIClient()
    
#     response = client.get(reverse('cont_usuario'))
    
#     assert response.status_code == 200
#     # assert response.status_code == 400 si esta mal algo


# @pytest.mark.django_db
# def test_inicio_sesion():
#     client = APIClient()
    
#     user_data = {
#             "first_name": "Emmanuel",
#             "last_name": "Castañeda",
#             "email": "moto.emacasta12@gmail.com",
#             "tipo_documento_usuario": "Cedula de ciudadania",
#             "genero_usuario": "Masculino",
#             "rol_usuario": "Administrador",
#             "numero_documento_usuario": 101010,
#             "password": "1234",
#             "username": "emmanuel_casta"
#     }
#     Usuario.objects.create_user(**user_data)
    
#     response = client.post(reverse('inicio_sesion'), {
#         'numero_documento_usuario': 101010,
#         'password': '1234'
#     }, format='json')
    
#     assert response.status_code == 200
#     # assert response.status_code == 400 si esta mal algo
#     assert 'token' in response.data



# @pytest.mark.django_db
# def test_validar_token():
#     client = APIClient()
    
#     # Crear usuario
#     user = Usuario.objects.create_user(username="emmanuel_casta", numero_documento_usuario=101010, password='1234')
    
#     # Generar token de acceso
#     refresh = RefreshToken.for_user(user)
#     access_token = str(refresh.access_token)
    
#     # Agregar el token en el header de la petición
#     client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
#     # Probar la vista protegida
#     response = client.get(reverse('protected_view'))
    
#     assert response.status_code == 200
#     # assert response.status_code == 400 si esta mal algo
#     assert response.data['message'] == 'Usuario autenticado correctamente'
