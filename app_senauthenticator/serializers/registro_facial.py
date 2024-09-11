from rest_framework import serializers


class RegistroFacialSerializer(serializers.Serializer):
    nombre_completo = serializers.CharField(max_length=30)
    numero_documento = serializers.CharField(max_length=30)
    face_register = serializers.ImageField()