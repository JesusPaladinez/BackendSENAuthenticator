
# Los serializadores convierten los diccionarios de python a un objeto json para que se puedan utilizar en una API

from rest_framework import serializers

# importacion de modelos
from app_senauthenticator.models import UsuarioExterno

# Serializador del Usuario
class UsuarioExternoSerializer(serializers.ModelSerializer):
    class Meta: # Se utiliza la clase Meta para definir la estructura del serializador
        model = UsuarioExterno # Se define el modelo que se va a serializar
        fields = '__all__' # Se indica que campos se van a serializar, en este caso todos los campos        
        # Se asignan los campos que serán requeridos en los formularios
        extra_kwargs = { 
            'tipo_documento_usuario_externo': {'required': True},
            'numero_documento_usuario_externo': {'required': True},
            'first_name': {'required': True},
            'oficina_usuario_externo': {'required': False},
        } 
    