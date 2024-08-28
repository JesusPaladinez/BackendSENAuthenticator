from rest_framework import serializers


class FaceLoginSerializer(serializers.Serializer):
    face_login = serializers.CharField()