from rest_framework import serializers

# importacion de modelos
from app_senauthenticator.models import PasswordReset

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model=PasswordReset
        fields='__all__'