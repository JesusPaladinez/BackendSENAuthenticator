# Los serializer convierten los datos a formato json, para que puedan ser utilizados a través de una API.

from rest_framework import serializers

# importacion de modelos
from app_senauthenticator.models import Oficina


class OficinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oficina
        fields = '__all__'
        extra_kwargs = {
            'nombre_oficina': {'required': True},
        } 