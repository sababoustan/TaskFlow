from rest_framework import serializers
from apps.workspaces.models import Workspace, WorkspaceInvitation
from apps.workspaces.choices import Role


class WorkspaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workspace
        fields = [
            'id',
            'title',
            'created_at',
        ]