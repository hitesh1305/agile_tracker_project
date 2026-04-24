from django.urls import path
from .views import project_stories

urlpatterns = [
    path('projects/<uuid:project_id>/stories/', project_stories),
]