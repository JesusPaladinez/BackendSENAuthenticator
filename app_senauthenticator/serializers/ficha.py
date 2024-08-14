# Los serializer convierten los datos a formato json, para que puedan ser utilizados a través de una API.

from rest_framework import serializers

# importacion de modelos
from app_senauthenticator.models import Ficha


class FichaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ficha
        fields = '__all__'
        extra_kwargs = {
            'numero_ficha': {'required': True},
            'aprendices_matriculados_ficha': {'required': True},
            'aprendices_actuales_ficha': {'required': True},
            'jornada_ficha': {'required': True},
            'programa_ficha': {'required': False},
        } 