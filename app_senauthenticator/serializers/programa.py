from rest_framework import serializers

# importacion de modelos
from app_senauthenticator.models import Programa


class ProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programa
        fields = '__all__'
        extra_kwargs = {
            'nombre_programa': {'required': True},
            'tipo_formacion_programa': {'required': True},
        }    