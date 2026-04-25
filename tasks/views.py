from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from stories.models import UserStory
from django.shortcuts import get_object_or_404
from .utils import mark_overdue_tasks

@api_view(['GET', 'POST'])
def story_tasks(request, story_id):

    mark_overdue_tasks()   # simulate background job

    

@api_view(['GET', 'POST'])
def story_tasks(request, story_id):
    story = get_object_or_404(UserStory, id=story_id)

    if request.method == 'GET':
        tasks = Task.objects.filter(user_story=story)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        data = request.data.copy()
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            try:
                task = serializer.save(user_story=story, created_by=request.user)
                return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

            except Exception as e:
                import traceback
                traceback.print_exc()
                return Response({"error": str(e)}, status=500)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # 🔒 ROLE CHECK
    if request.user != task.user_story.project.owner:
        return Response({"error": "Permission denied"}, status=403)

    status_value = request.POST.get("status")

    if status_value not in ['TODO', 'IN_PROGRESS', 'DONE']:
        return Response({"error": "Invalid status"}, status=400)

    task.status = status_value
    task.save()

    return Response({"message": "Task updated"})