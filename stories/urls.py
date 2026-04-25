from django.urls import path
from .views import project_stories
from .views import story_detail_view
from .views import create_task_view
from .views import create_story_view
from .views import update_story_view

urlpatterns = [
    path('projects/<uuid:project_id>/stories/', project_stories),
    path('stories/<uuid:story_id>/', story_detail_view),
    path('stories/<uuid:story_id>/create-task/', create_task_view),
    path('projects/<uuid:project_id>/create-story/', create_story_view),
    path('stories/<uuid:story_id>/update/', update_story_view),
]