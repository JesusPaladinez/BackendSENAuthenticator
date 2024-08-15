from rest_framework import serializers


class AutenticacionFacial(serializers.Serializer):
    current_face = serializers.CharField()