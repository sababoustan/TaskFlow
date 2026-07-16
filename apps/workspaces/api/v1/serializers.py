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


class InvitationsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)
    role = serializers.ChoiceField(Role.choices)

    class Meta:
        model = WorkspaceInvitation
        fields = [
            'email',
            'role',
        ]