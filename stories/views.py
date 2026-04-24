from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserStory
from .serializers import UserStorySerializer
from projects.models import Project
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

@api_view(['GET', 'POST'])
def project_stories(request, project_id):
    # safer way to fetch project
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'GET':
        stories = UserStory.objects.filter(project=project)
        serializer = UserStorySerializer(stories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        serializer = UserStorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project, created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)