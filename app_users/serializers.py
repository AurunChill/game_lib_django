# Third-party imports
from rest_framework import serializers

# Project imports
from app_users import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserModel
        fields = ['id', 'username', 'email', 'image']