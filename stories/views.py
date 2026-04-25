from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserStory
from .serializers import UserStorySerializer
from projects.models import Project
from django.shortcuts import render, get_object_or_404
from tasks.models import Task
from django.shortcuts import redirect
from tasks.models import Task
from django.contrib.auth.decorators import login_required
from tasks.utils import mark_overdue_tasks

@login_required
def create_task_view(request, story_id):
    story = get_object_or_404(UserStory, id=story_id)

    # 🔒 STRICT PERMISSION CHECK
    if request.user != story.project.owner or not request.user.is_staff:
        return redirect(f'/stories/{story.id}/')

    if request.method == 'POST':
        Task.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            due_date=request.POST.get('due_date') or None,
            status='TODO',
            user_story=story,
            created_by=request.user
        )

    return redirect(f'/stories/{story.id}/')


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
    

@login_required
def story_detail_view(request, story_id):
    story = get_object_or_404(UserStory, id=story_id)

    mark_overdue_tasks()  # keep this

    tasks = Task.objects.filter(user_story=story)

    return render(request, 'story_detail.html', {
        'story': story,
        'tasks': tasks
    })

def create_story_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user != project.owner or not request.user.is_staff:
        return redirect(f'/projects/{project.id}/')

    if request.method == 'POST':
        UserStory.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            status='TODO',
            project=project,
            created_by=request.user
        )

    return redirect(f'/projects/{project.id}/')

def update_story_view(request, story_id):
    story = get_object_or_404(UserStory, id=story_id)

    # 🔒 permission
    if request.user != story.project.owner or not request.user.is_staff:
        return redirect(f'/projects/{story.project.id}/')

    if request.method == 'POST':
        status = request.POST.get('status')

        if status in ['TODO', 'IN_PROGRESS', 'DONE']:
            story.status = status
            story.save()

    return redirect(f'/projects/{story.project.id}/')