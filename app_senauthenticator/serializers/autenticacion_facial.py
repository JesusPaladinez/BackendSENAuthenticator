from rest_framework import serializers


class AutenticacionFacialSerializer(serializers.Serializer):
    current_face = serializers.CharField()