# import pytest
# from django.core.files.uploadedfile import SimpleUploadedFile
# from rest_framework.test import APIClient
# from app_senauthenticator.models import Objeto
# from app_senauthenticator.models import Usuario

# from django.core.files.uploadedfile import SimpleUploadedFile
# from PIL import Image
# import io

# from django.urls import reverse

# @pytest.mark.django_db
# def test_crear_objeto():
#     usuario = Usuario.objects.create_user(
#         last_name= "Castañeda",
#         email= "moto.emacasta12@gmail.com",
#         tipo_documento_usuario= "Cedula de ciudadania",
#         genero_usuario= "Masculino",
#         rol_usuario= "Administrador",
#         numero_documento_usuario= 101010,
#         password= "1234",
#         username = "emmanuel_casta"
#     )

#     objeto = APIClient()

#     # Crear una imagen simulada
#     img = Image.new('RGB', (100, 100), color = (73, 109, 137))
#     img_io = io.BytesIO()
#     img.save(img_io, format='JPEG')
#     img_io.seek(0)

#     foto = SimpleUploadedFile("foto.jpg", img_io.read(), content_type="image/jpeg")

#     data = {
#         'marca_objeto': 'Hp',
#         'modelo_objeto': 'sq14',
#         'descripcion_objeto': 'portatil pequeño',
#         'foto_objeto': foto,
#         'usuario_objeto': usuario.id,
#     }

#     response = objeto.post(reverse('cont_objeto'), data, format='multipart')
#     print(response.data)

#     assert response.status_code == 201

#     # assert response.status_code == 400 si esta mal algo

# @pytest.mark.django_db
# def test_obtener_objetos():
#     objeto = APIClient()
    
#     response = objeto.get(reverse('cont_objeto'))
    
#     assert response.status_code == 200
#     # assert response.status_code == 400 si esta mal algo


# @pytest.mark.django_db
# def test_actualizar_objeto():
#     usuario  = Usuario.objects.create_user(
#             last_name= "Castañeda",
#             email= "moto.emacasta12@gmail.com",
#             tipo_documento_usuario= "Cedula de ciudadania",
#             genero_usuario= "Masculino",
#             rol_usuario= "Administrador",
#             numero_documento_usuario= 101010,
#             password= "1234",
#             username = "emmanuel_casta"
#         )

#     # Crear un programa y una ficha
#     objeto = Objeto.objects.create(
#             marca_objeto= "Asus",
#             modelo_objeto= "sq33",
#             descripcion_objeto= "Grande",
#             foto_objeto= "",
#             usuario_objeto= usuario,
#     )
    
#     client = APIClient()
#     data = {
#             'marca_objeto': 'Asus',
#             'modelo_objeto': 'sq44',
#             'descripcion_objeto': 'Grande',
#             'foto_objeto': '',
#             'usuario_objeto': usuario.id,
#     }

#     response = client.put(reverse('cont_objeto', args=[objeto.pk]), data, format='json')
    
#     assert response.status_code == 200
#     # Verificamos que los cambios se hayan aplicado
#     objeto.refresh_from_db()
#     assert objeto.modelo_objeto == 'sq44'



# @pytest.mark.django_db
# def test_eliminar_objeto():
#     usuario  = Usuario.objects.create_user(
#             last_name= "Castañeda",
#             email= "moto.emacasta12@gmail.com",
#             tipo_documento_usuario= "Cedula de ciudadania",
#             genero_usuario= "Masculino",
#             rol_usuario= "Administrador",
#             numero_documento_usuario= 101010,
#             password= "1234",
#             username = "emmanuel_casta"
#         )
    
#     objeto = Objeto.objects.create(
#             marca_objeto= "Asus",
#             modelo_objeto= "sq33",
#             descripcion_objeto= "Grande",
#             foto_objeto= "",
#             usuario_objeto= usuario,
#     )
    
#     client = APIClient()

#     # Hacemos la petición DELETE para eliminar la ficha
#     response = client.delete(reverse('cont_objeto', args=[objeto.pk]))
    
#     assert response.status_code == 204
#     # Verificamos que la ficha haya sido eliminada
    
#     assert not Objeto.objects.filter(pk=objeto.pk).exists()