from rest_framework import serializers

# importacion de modelos
from app_senauthenticator.models import Objeto


class ObjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Objeto
        fields = '__all__'
        extra_kwargs = {
            'marca_objeto': {'required': True},
            'modelo_objeto': {'required': True},
            'descripcion_objeto': {'required': True},
            'foto_objeto': {'required': True},
            'usuario_objeto': {'required': False},
        } 