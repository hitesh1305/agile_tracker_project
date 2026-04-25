from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from stories.models import UserStory
from tasks.models import Task
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    stories = UserStory.objects.filter(project=project)

    tasks = Task.objects.filter(user_story__project=project)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='DONE').count()

    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)
    else:
        progress = 0   # VERY IMPORTANT

    return render(request, 'project_detail.html', {
        'project': project,
        'stories': stories,
        'progress': progress
    })


@api_view(['GET', 'POST'])
def get_projects(request):

    if request.method == 'GET':
        projects = Project.objects.all().order_by('-created_at')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
        
            user = User.objects.first()
            serializer.save(owner=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@login_required
def project_list_view(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})


@login_required
def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    stories = UserStory.objects.filter(project=project).order_by('-created_at')

    return render(request, 'project_detail.html', {
        'project': project,
        'stories': stories
    })

def create_project_view(request):
    if request.method == 'POST':
        Project.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            owner=request.user
        )
    return redirect('/')