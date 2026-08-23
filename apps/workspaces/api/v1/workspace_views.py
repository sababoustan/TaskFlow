from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from apps.workspaces.permissions import IsWorkspaceOwner
from apps.workspaces.models import Workspace

from .serializers import WorkspaceSerializer


class WorkspaceViewSet(ModelViewSet):
    serializer_class = WorkspaceSerializer
    search_fields = ["title"]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated, IsWorkspaceOwner]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user

        return Workspace.objects.filter(
            Q(owner=user) | Q(memberships__user=user)
        ).distinct()
