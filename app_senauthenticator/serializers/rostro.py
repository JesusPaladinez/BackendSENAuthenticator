from rest_framework import serializers


class RostroSerializer(serializers.Serializer):
    current_face = serializers.CharField()