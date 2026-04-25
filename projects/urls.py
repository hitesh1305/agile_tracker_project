from django.urls import path
from .views import get_projects
from .views import project_list_view
from .views import project_detail_view


urlpatterns = [
    path('projects/', get_projects),
    path('', project_list_view),
    path('projects/<uuid:project_id>/', project_detail_view),
]