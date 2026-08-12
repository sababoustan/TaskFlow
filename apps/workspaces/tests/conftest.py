import pytest
from apps.workspaces.models import WorkspaceInvitation, Membership
from apps.users.models import User
from apps.workspaces.choices import Role


@pytest.fixture
def invited_user(db):
    return User.objects.create_user(
        email="sadafboustan@gmail.com",
        password="StrongPassword123",
        is_verified=True,
    )


@pytest.fixture
def workspace_invitation(user, workspace, invited_user):
    return WorkspaceInvitation.objects.create(
        invited_by=user,
        workspace=workspace,
        user=invited_user,
        role=Role.MEMBER
    )


@pytest.fixture
def membership(workspace_invitation):
    return Membership.objects.create(
        user=workspace_invitation.user,
        workspace=workspace_invitation.workspace,
        role=workspace_invitation.role
    )