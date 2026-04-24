from rest_framework import serializers
from .models import UserStory

class UserStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStory
        fields = [
            'id',
            'title',
            'description',
            'status',
            'assignee',
            'created_at'
        ]