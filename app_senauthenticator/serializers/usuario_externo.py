from rest_framework import serializers
from app_senauthenticator.models import UsuarioExterno

# Serializador del Usuario
class UsuarioExternoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioExterno
        fields = '__all__'
        extra_kwargs = {
            'tipo_documento_usuario_externo': {'required': True},
            'numero_documento_usuario_externo': {'required': True},
            'first_name': {'required': True},
            'oficina_usuario_externo': {'required': True},
            'descripcion_usuario_externo':{'required':False},
            'password': {'required': False, 'write_only': True},  # El campo password es opcional
            'username': {'required': False}  # El campo username también es opcional
        }

    def validate_password(self, value):
        return value  # Devuelve el valor de password sin validación para que sea opcional
