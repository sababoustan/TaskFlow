from django.urls import path, include


app_name = 'projects'

urlpatterns = [
    path('projects/', include('apps.projects.api.v1.urls')),
]