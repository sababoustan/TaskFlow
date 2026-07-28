from rest_framework import serializers
from apps.workspaces.models import Workspace, WorkspaceInvitation, Membership
from apps.workspaces.choices import Role


class WorkspaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workspace
        fields = [
            'id',
            'title',
            'created_at',
        ]


class InvitationCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)
    role = serializers.ChoiceField(Role.choices)

    class Meta:
        model = WorkspaceInvitation
        fields = [
            'email',
            'role',
        ]


class InvitationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    invited_by = serializers.EmailField(source="invited_by.email",
                                        read_only=True)

    class Meta:
        model = WorkspaceInvitation
        fields = [
            'id',
            'email',
            'invited_by',
            'role',
            'status',
            'created_at',
        ]


class MembershipListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Membership
        fields = [
            'id',
            'email',
            'role',
            'joined_at',
        ]


class MembershipUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = [
            'role',
        ]