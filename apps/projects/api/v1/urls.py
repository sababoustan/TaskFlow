from django.urls import path

# from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    StatusViewSet,
    WorkflowStatusViewSet,
    WorkflowViewSet,
    SprintViewSet
)

app_name = "api/v1"


urlpatterns = [
    path(
        "statuses/",
        StatusViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "statuses/<int:pk>/",
        StatusViewSet.as_view(
            {
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "<int:workspace_id>/workflows/",
        WorkflowViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "<int:workspace_id>/workflows/<int:workflow_id>/",
        WorkflowViewSet.as_view({"patch": "update", "delete": "destroy"}),
    ),
    path(
        "<int:workspace_id>/projects/",
        ProjectViewSet.as_view({"get": "list"}),
    ),
    path(
        "<int:workspace_id>/workflows/<int:workflow_id>/projects/",
        ProjectViewSet.as_view({"post": "create"}),
    ),
    path(
        "<int:workspace_id>/projects/<int:project_id>/",
        ProjectViewSet.as_view({"patch": "update"}),
    ),
    path(
        "<int:workflow_id>/workflow_status/",
        WorkflowStatusViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "workflow_status/<int:workflow_status_id>/",
        WorkflowStatusViewSet.as_view(
            {
                "patch": "update",
                "delete": "destroy"
                }
            ),
    ),
    path(
        "workspaces/<int:workspace_id>/projects/<int:project_id>/sprints/",
        SprintViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "workspaces/<int:workspace_id>/projects/<int:project_id>/sprints/<int:sprint_id>/",
        SprintViewSet.as_view({
            "get": "retrieve",
            "patch": "update",
            "delete": "destroy"}),
        ),
]
