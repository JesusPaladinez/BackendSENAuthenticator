from rest_framework import serializers


class RegistroFacialSerializer(serializers.Serializer):
    numero_documento = serializers.CharField(max_length=30)
    face_register = serializers.ImageField()