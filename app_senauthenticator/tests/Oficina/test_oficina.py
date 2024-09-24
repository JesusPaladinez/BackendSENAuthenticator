# import pytest
# from rest_framework.test import APIClient
# from app_senauthenticator.models import Oficina
# from django.urls import reverse

# @pytest.mark.django_db
# def test_crear_oficina():
#     oficina = APIClient()
#     data = {
#         'nombre_oficina': 'Software 1',
#     }

#     response = oficina.post(reverse('cont_oficina'), data, format='json')
#     print(response.data)

#     assert response.status_code == 201
#     # assert response.status_code == 400 si esta mal algo
    
#     # assert Usuario.objects.filter(numero_documento_usuario='12345678').exists()

# @pytest.mark.django_db
# def test_obtener_oficinas():
#     oficina = APIClient()
    
#     response = oficina.get(reverse('cont_oficina'))
    
#     assert response.status_code == 200
#     # assert response.status_code == 400 si esta mal algo


# @pytest.mark.django_db
# def test_actualizar_oficina():
#     oficina = Oficina.objects.create(
#         nombre_oficina='Software 1',
#     )
    
#     client = APIClient()
#     data = {
#         'nombre_oficina': 'Software 2',            # Cambiamos la jornada
#     }

#     response = client.put(reverse('cont_oficina', args=[oficina.pk]), data, format='json')
    
#     assert response.status_code == 200
#     # Verificamos que los cambios se hayan aplicado
#     oficina.refresh_from_db()
#     assert oficina.nombre_oficina == "Software 2"


# @pytest.mark.django_db
# def test_eliminar_oficina():
#     oficina = Oficina.objects.create(
#         nombre_oficina='Software 1',
#     )
    
#     client = APIClient()

#     # Hacemos la petición DELETE para eliminar la ficha
#     response = client.delete(reverse('cont_oficina', args=[oficina.pk]))
    
#     assert response.status_code == 204
#     # Verificamos que la ficha haya sido eliminada
#     assert not Oficina.objects.filter(pk=oficina.pk).exists()
