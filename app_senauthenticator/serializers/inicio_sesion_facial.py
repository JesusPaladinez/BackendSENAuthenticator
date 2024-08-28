from rest_framework import serializers


class InicioSesionSerializer(serializers.Serializer):
    face_login = serializers.ImageField()