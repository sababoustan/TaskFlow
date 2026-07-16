from django.urls import path, include


app_name = 'workspaces'

urlpatterns = [
    path('workspaces/', include('apps.workspaces.api.v1.urls')),
]