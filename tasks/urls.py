from django.urls import path
from .views import story_tasks
from .views import update_task_view

urlpatterns = [
    path('stories/<uuid:story_id>/tasks/', story_tasks),
    path('tasks/<uuid:task_id>/update-ui/', update_task_view),
]