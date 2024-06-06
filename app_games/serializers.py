# Third-party imports
from rest_framework import serializers

# Project imports
from app_games import models


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommentModel
        fields = ['id', 'user', 'game', 'text', 'date', 'votes', 'reply_to']