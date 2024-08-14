from rest_framework import serializers

# importacion de modelos
from app_senauthenticator.models import RegistroFacial


class RegistroFacialSerializer(serializers.ModelSerializer):
    class Meta: 
        model = RegistroFacial 
        fields = '__all__' 
        extra_kwargs = {
            'datos_biometricos_registro': {'required': True},
            'fecha_hora_registro': {'required': False},
            'usuario_registro_facial': {'required': False},
        } 