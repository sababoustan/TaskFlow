import pytest


@pytest.mark.django_db
def test_workspace_created(workspace):
    assert workspace.owner is not None
    assert workspace.title == "python"
    assert workspace.slug == "python"


@pytest.mark.django_db
def test_workspace_invitation(workspace, invited_user, workspace_invitation):
    assert workspace_invitation.invited_by is not None
    assert workspace_invitation.workspace.id == workspace.id
    assert workspace_invitation.user == invited_user
    assert workspace_invitation.role == "member"


@pytest.mark.django_db
def test_membership(membership, workspace_invitation):
    assert membership.user == workspace_invitation.user
    assert membership.workspace == workspace_invitation.workspace
    assert membership.role == workspace_invitation.role
