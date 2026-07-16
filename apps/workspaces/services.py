from apps.workspaces.models import WorkspaceInvitation, Workspace, Membership
from apps.users.models import User
from apps.workspaces.choices import InvitationStatus, Role
from django.core.exceptions import ValidationError
from .permissions import has_workspace_role
from django.shortcuts import get_object_or_404



def invite_user_to_workspace(*, invited_by, workspace_id, validated_data):
    email = validated_data["email"]
    role = validated_data["role"]
    workspace = Workspace.objects.filter(id=workspace_id).first()
    print(workspace)
    workspace = get_object_or_404(
        Workspace,
        id=workspace_id,
    )
    has_workspace_role(
        workspace=workspace,
        user=invited_by,
        allowed_roles=[Role.ADMIN],
    )
    print(email)
    user = get_object_or_404(
        User,
        email=email,
    )
    if Membership.objects.filter(
        workspace=workspace,
        user=user,
    ).exists():
        raise ValidationError(
            {
                "email": "User is already a member."
            }
        )

    if WorkspaceInvitation.objects.filter(
        workspace=workspace,
        user=user,
        status=InvitationStatus.PENDING,
    ).exists():
        raise ValidationError(
            {
                "email": "User already has a pending invitation."
            }
        )
    return WorkspaceInvitation.objects.create(
        invited_by=invited_by,
        workspace=workspace,
        user=user,
        role=role,
    )