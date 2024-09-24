# import pytest
# from rest_framework.test import APIClient
# from app_senauthenticator.models import Programa

# from django.urls import reverse
# from rest_framework_simplejwt.tokens import RefreshToken

# @pytest.mark.django_db
# def test_crear_programa():
#     progam = APIClient()
#     data = {
#             'nombre_programa': "Analisis y desarrollo de software",
#             'tipo_formacion_programa': "Tecnologo",
#     }

#     response = progam.post(reverse('cont_programa'), data, format='json')
#     print(response.data)  

#     assert response.status_code == 201
#     # assert response.status_code == 400 si esta mal algo

# @pytest.mark.django_db
# def test_obtener_programas():
#     progam = APIClient()
    
#     response = progam.get(reverse('cont_programa'))
    
#     assert response.status_code == 200
#     # assert response.status_code == 400 si esta mal algo


# @pytest.mark.django_db
# def test_actualizar_programa():
#     # Crear un programa y una ficha
#     progam = Programa.objects.create(
#             nombre_programa= "Analisis y desarrollo de software",
#             tipo_formacion_programa= "Tecnologo",
#     )
    
#     client = APIClient()
#     data = {
#             'nombre_programa': "Animacion 3D",
#             'tipo_formacion_programa': "Tecnico",        # Cambiamos la jornada
#     }

#     response = client.put(reverse('cont_programa', args=[progam.pk]), data, format='json')
    
#     assert response.status_code == 200
#     # Verificamos que los cambios se hayan aplicado
#     progam.refresh_from_db()
#     assert progam.nombre_programa == 'Animacion 3D'
#     assert progam.tipo_formacion_programa == 'Tecnico'


# @pytest.mark.django_db
# def test_eliminar_programa():
#     progam = Programa.objects.create(
#             nombre_programa= "Analisis y desarrollo de software",
#             tipo_formacion_programa= "Tecnologo",
#     )
    
#     client = APIClient()

#     # Hacemos la petición DELETE para eliminar la ficha
#     response = client.delete(reverse('cont_programa', args=[progam.pk]))
    
#     assert response.status_code == 204
#     # Verificamos que la ficha haya sido eliminada
    
#     assert not Programa.objects.filter(pk=progam.pk).exists()