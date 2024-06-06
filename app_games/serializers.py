# Third-party imports
from rest_framework import serializers

# Project imports
from app_games import models
from app_users.serializers import UserSerializer
from app_users.models import UserModel


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GameModel
        fields = ['id', 'title', 'description', 'author', 'release_date', 'total_price', 'discount', 'image']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    game = GameSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all(), write_only=True, source='user')
    game_id = serializers.PrimaryKeyRelatedField(
        queryset=models.GameModel.objects.all(), write_only=True, source='game')

    class Meta:
        model = models.CommentModel
        fields = ['id', 'user', 'user_id', 'game', 'game_id', 'text', 'date', 'votes', 'reply_to']