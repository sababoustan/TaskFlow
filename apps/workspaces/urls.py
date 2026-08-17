from django.urls import include, path

app_name = "workspaces"

urlpatterns = [
    path("workspaces/", include("apps.workspaces.api.v1.urls")),
]
