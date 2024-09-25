import pytest
from rest_framework.test import APIClient
from app_senauthenticator.models import UsuarioExterno
from app_senauthenticator.models import Oficina
from django.urls import reverse

@pytest.mark.django_db
def test_crear_usuario_externo():
    oficina = Oficina.objects.create(nombre_oficina='Software 1')

    usuario_externo = APIClient()
    data = {
        'tipo_documento_usuario': "Cédula de ciudadanía",
        'numero_documento_usuario': "1059235737",
        'first_name': 'Miguel Angel Astudillo',
        'oficina_usuario': oficina.id
    }

    response = usuario_externo.post(reverse('cont_usuario_externo'), data, format='json')
    print(response.data)

    assert response.status_code == 201


@pytest.mark.django_db
def test_obtener_usuario_externos():
    usuario_externo = APIClient()
    
    response = usuario_externo.get(reverse('cont_usuario_externo'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_usuario_externo():
    # Crear un programa y una ficha
    oficina = Oficina.objects.create(oficina_usuario='ADSO')
    usuario_externo = UsuarioExterno.objects.create(
        tipo_documento_usuario='Cédula de ciudadanía',
        numero_documento_usuario="1059235737",
        first_name="Miguel",
        oficina_usuario=oficina
    )
    
    client = APIClient()
    data = {
        'tipo_documento_usuario': 'Cédula de ciudadanía',
        'numero_documento_usuario': "1059235737",  
        'first_name': "Daniel",      
        'oficina_usuario': oficina.id
    }

    response = client.put(reverse('cont_usuario_externo', args=[usuario_externo.pk]), data, format='json')
    
    assert response.status_code == 200
    # Verificamos que los cambios se hayan aplicado
    usuario_externo.refresh_from_db()
    assert usuario_externo.aprendices_actuales_ficha == "Daniel"


@pytest.mark.django_db
def test_usuario_externo():
    oficina = Oficina.objects.create(oficina_usuario='ADSO')
    usuario_externo = UsuarioExterno.objects.create(
        tipo_documento_usuario='Cédula de ciudadanía',
        numero_documento_usuario="1059235737",
        first_name="Miguel",
        oficina_usuario=oficina
    )
    
    client = APIClient()

    # Hacemos la petición DELETE para eliminar la ficha
    response = client.delete(reverse('cont_usuario_externo', args=[usuario_externo.pk]))
    
    assert response.status_code == 204
    # Verificamos que la ficha haya sido eliminada
    assert not UsuarioExterno.objects.filter(pk=usuario_externo.pk).exists()
