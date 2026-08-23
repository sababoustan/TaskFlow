import pytest
from django.db import IntegrityError

from apps.workspaces.choices import Role, InvitationStatus
from apps.workspaces.models import Membership, WorkspaceInvitation, Workspace


@pytest.mark.django_db
def test_workspace_created(workspace):
    assert workspace.owner is not None
    assert workspace.title == "python"
    assert workspace.slug == "python"


@pytest.mark.django_db
def test_workspace_generates_unique_slug(user, workspace):
    another_workspace = Workspace.objects.create(
        owner=user,
        title="python",
    )

    assert another_workspace.slug == "python-1"


@pytest.mark.django_db
def test_workspace_invitation(
    workspace,
    invited_user,
    workspace_invitation,
):
    assert workspace_invitation.invited_by is not None
    assert workspace_invitation.workspace == workspace
    assert workspace_invitation.user == invited_user
    assert workspace_invitation.role == Role.MEMBER
    assert workspace_invitation.status == InvitationStatus.PENDING


@pytest.mark.django_db
def test_membership(membership, workspace_invitation):
    assert membership.user == workspace_invitation.user
    assert membership.workspace == workspace_invitation.workspace
    assert membership.role == workspace_invitation.role


@pytest.mark.django_db
def test_membership_unique_user_per_workspace(
    membership,
):
    with pytest.raises(IntegrityError):
        Membership.objects.create(
            user=membership.user,
            workspace=membership.workspace,
            role=Role.MEMBER,
        )


@pytest.mark.django_db
def test_pending_workspace_invitation_unique_per_user_and_workspace(
    workspace_invitation,
):
    with pytest.raises(IntegrityError):
        WorkspaceInvitation.objects.create(
            invited_by=workspace_invitation.invited_by,
            workspace=workspace_invitation.workspace,
            user=workspace_invitation.user,
            role=Role.MEMBER,
            status=InvitationStatus.PENDING,
        )