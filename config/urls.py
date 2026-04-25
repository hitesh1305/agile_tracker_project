from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Frontend (UI)
    path('', include('projects.urls')),
    path('', include('stories.urls')), 

    # API
    path('api/', include('projects.urls')),
    path('api/', include('stories.urls')),
    path('api/', include('tasks.urls')),

    path('api-auth/', include('rest_framework.urls')),

    path('accounts/', include('django.contrib.auth.urls')),
]