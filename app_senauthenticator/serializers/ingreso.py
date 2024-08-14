from rest_framework import serializers

# importacion de modelos
from app_senauthenticator.models import Ingreso


class IngresoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingreso
        fields = '__all__'
        extra_kwargs = {
            'datos_biometricos_ingreso': {'required': True},
            'fecha_hora_ingreso': {'required': False},
            'usuario_ingreso': {'required': False},
        } 