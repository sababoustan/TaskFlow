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
    workspace = get_object_or_404(
        Workspace,
        id=workspace_id,
    )
    has_workspace_role(
        workspace=workspace,
        user=invited_by,
        allowed_roles=[Role.ADMIN],
    )
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


def accept_invitation(*, invitation):
    if invitation.status != InvitationStatus.PENDING:
        raise ValidationError(
            {
                "message": "This invitation has already been processed."
            }
        )
    if Membership.objects.filter(
        workspace=invitation.workspace,
        user=invitation.user,
    ).exists():
        raise ValidationError(
            {
                "message": "User is already a member of this workspace."
            }
        )
    membership = Membership.objects.create(
        user=invitation.user,
        workspace=invitation.workspace,
        role=invitation.role,
    )

    invitation.status = InvitationStatus.ACCEPTED
    invitation.save(update_fields=["status"])
    return membership


def reject_invitation(*, invitation):
    if invitation.status != InvitationStatus.PENDING:
        raise ValidationError(
            {
                "message": "This invitation has already been processed."
            }
        )
    invitation.status = InvitationStatus.REJECTED
    invitation.save(update_fields=["status"])
    return invitation


def cancel_invitation(*, invitation):
    if invitation.status != InvitationStatus.PENDING:
        raise ValidationError(
            {
                "message": "This invitation has already been processed."
            }
        )
    invitation.status = InvitationStatus.CANCELLED
    invitation.save(update_fields=["status"])
    return invitation


def update_membership_role(*, membership, workspace_id, updated_by, role):
    workspace = get_object_or_404(
            Workspace,
            id=workspace_id,
        )
    has_workspace_role(
        workspace=workspace,
        user=updated_by,
        allowed_roles=[Role.ADMIN],
    )
    membership.role = role
    membership.save(update_fields=["role"])
    return membership


def remove_workspace_member(*, membership, workspace_id, updated_by):
    workspace = get_object_or_404(
            Workspace,
            id=workspace_id
        )
    has_workspace_role(
        workspace=workspace,
        user=updated_by,
        allowed_roles=[Role.ADMIN],
    )
    membership.delete()