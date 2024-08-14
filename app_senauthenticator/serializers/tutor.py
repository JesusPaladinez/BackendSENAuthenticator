from rest_framework import serializers

# importacion de modelos
from app_senauthenticator.models import Tutor


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'
        extra_kwargs = {
            'nombre_tutor': {'required': True},
            'apellido_tutor': {'required': True},
            'tipo_documento_tutor': {'required': True},
            'numero_documento_tutor': {'required': True},
            'celular_tutor': {'required': True},
            'genero_tutor': {'required': True},
            'parentezco_tutor': {'required': True},
            'usuario_tutor': {'required': False},
        }