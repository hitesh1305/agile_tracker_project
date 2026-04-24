from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from stories.models import UserStory
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


@api_view(['GET', 'POST'])
def story_tasks(request, story_id):

    story = get_object_or_404(UserStory, id=story_id)

    if request.method == 'GET':
        tasks = Task.objects.filter(user_story=story)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.first()  # temp fix
            serializer.save(user_story=story, created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)