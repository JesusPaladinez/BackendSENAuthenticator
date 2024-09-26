# import pytest
# from rest_framework.test import APIClient
# from app_senauthenticator.models import Ficha
# from app_senauthenticator.models import Programa
# from django.urls import reverse

# @pytest.mark.django_db
# def test_crear_ficha():
#     programa = Programa.objects.create(nombre_programa='ADSO')

#     ficha = APIClient()
#     data = {
#         # 'numero_ficha': '2669742',
#         'aprendices_matriculados_ficha': 28,
#         'aprendices_actuales_ficha': 23,
#         'jornada_ficha': 'Mañana',
#         'programa_ficha': programa.id
#     }

#     response = ficha.post(reverse('cont_ficha'), data, format='json')
#     print(response.data)

#     assert response.status_code == 201
#     # assert response.status_code == 400 si esta mal algo
    
#     # assert Usuario.objects.filter(numero_documento_usuario='12345678').exists()

# @pytest.mark.django_db
# def test_obtener_fichas():
#     ficha = APIClient()
    
#     response = ficha.get(reverse('cont_ficha'))
#     assert response.status_code == 200
# #     # assert response.status_code == 400 si esta mal algo


# @pytest.mark.django_db
# def test_actualizar_ficha():
#     # Crear un programa y una ficha
#     programa = Programa.objects.create(nombre_programa='ADSO')
#     ficha = Ficha.objects.create(
#         numero_ficha='2669742',
#         aprendices_matriculados_ficha=28,
#         aprendices_actuales_ficha=23,
#         jornada_ficha='Mañana',
#         programa_ficha=programa
#     )
    
#     client = APIClient()
#     data = {
#         'numero_ficha': '2669742',
#         'aprendices_matriculados_ficha': 30,  # Actualizamos este campo
#         'aprendices_actuales_ficha': 25,      # Y este también
#         'jornada_ficha': 'Tarde',             # Cambiamos la jornada
#         'programa_ficha': programa.id
#     }

#     response = client.put(reverse('cont_ficha', args=[ficha.pk]), data, format='json')
    
#     assert response.status_code == 200
#     # Verificamos que los cambios se hayan aplicado
#     ficha.refresh_from_db()
#     assert ficha.aprendices_matriculados_ficha == 30
#     assert ficha.aprendices_actuales_ficha == 25
#     assert ficha.jornada_ficha == 'Tarde'


# @pytest.mark.django_db
# def test_eliminar_ficha():
#     programa = Programa.objects.create(nombre_programa='ADSO')
#     ficha = Ficha.objects.create(
#         numero_ficha='2669742',
#         aprendices_matriculados_ficha=28,
#         aprendices_actuales_ficha=23,
#         jornada_ficha='Mañana',
#         programa_ficha=programa
#     )
    
#     client = APIClient()

#     # Hacemos la petición DELETE para eliminar la ficha
#     response = client.delete(reverse('cont_ficha', args=[ficha.pk]))
    
#     assert response.status_code == 204
#     # Verificamos que la ficha haya sido eliminada
#     assert not Ficha.objects.filter(pk=ficha.pk).exists()
