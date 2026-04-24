from django.urls import path
from .views import story_tasks

urlpatterns = [
    path('stories/<uuid:story_id>/tasks/', story_tasks),
]