from django.urls import include, path

app_name = "projects"

urlpatterns = [
    path("projects/", include("apps.projects.api.v1.urls")),
]
