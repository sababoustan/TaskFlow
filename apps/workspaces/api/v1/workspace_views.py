from rest_framework.viewsets import ModelViewSet
from .serializers import WorkspaceSerializer
from rest_framework.permissions import IsAuthenticated
from apps.workspaces.models import Workspace
from django.db.models import Q


class WorkspaceViewSet(ModelViewSet):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user

        return Workspace.objects.filter(
            Q(owner=user) |
            Q(memberships__user=user)).distinct()