import pytest
from apps.workspaces.models import WorkspaceInvitation, Membership
from apps.workspaces.choices import (
    Role,
    InvitationStatus,
)


@pytest.mark.django_db
def test_create_invitation(
    client,
    user,
    workspace,
    invited_user,
):
    login_response = client.post(
        "/api/v1/auth/login/",
        {
            "email": user.email,
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert login_response.status_code == 200
    access = login_response.data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
    )

    response = client.post(
        f"/api/v1/workspaces/{workspace.id}/invitations/",
        {
            "email": invited_user.email,
            "role": Role.MEMBER,
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["messages"] == "The user was successfully invited."

    invitation = WorkspaceInvitation.objects.get(
        workspace=workspace,
        user=invited_user,
    )

    assert invitation.invited_by == user
    assert invitation.workspace == workspace
    assert invitation.user == invited_user
    assert invitation.role == Role.MEMBER
    assert invitation.status == InvitationStatus.PENDING


@pytest.mark.django_db
def test_list_invitations(
    client,
    user,
    workspace,
    workspace_invitation,
):
    login_response = client.post(
        "/api/v1/auth/login/",
        {
            "email": user.email,
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert login_response.status_code == 200
    access = login_response.data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
    )

    response = client.get(
        f"/api/v1/workspaces/{workspace.id}/invitations/",
    )

    assert response.status_code == 200

    invitation = response.data["data"][0]

    assert invitation["id"] == workspace_invitation.id
    assert invitation["email"] == workspace_invitation.user.email
    assert invitation["invited_by"] == workspace_invitation.invited_by.email
    assert invitation["role"] == workspace_invitation.role


@pytest.mark.django_db
def test_accept_invitation(
    client,
    workspace,
    invited_user,
    workspace_invitation,
):
    login_response = client.post(
        "/api/v1/auth/login/",
        {
            "email": invited_user.email,
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert login_response.status_code == 200
    access = login_response.data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
    )

    assert not Membership.objects.filter(
        workspace=workspace,
        user=invited_user,
    ).exists()

    response = client.post(
        f"/api/v1/workspaces/invitations/{workspace_invitation.id}/accept/",
    )

    assert response.status_code == 201
    assert response.data["message"] == "Invitation accepted successfully."

    membership = Membership.objects.get(
        workspace=workspace,
        user=invited_user,
    )

    assert membership.workspace == workspace
    assert membership.user == invited_user
    assert membership.role == Role.MEMBER

    workspace_invitation.refresh_from_db()

    assert workspace_invitation.status == InvitationStatus.ACCEPTED


@pytest.mark.django_db
def test_reject_invitation(
    client,
    invited_user,
    workspace_invitation,
):
    login_response = client.post(
        "/api/v1/auth/login/",
        {
            "email": invited_user.email,
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert login_response.status_code == 200
    access = login_response.data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
    )
    response = client.post(
        f"/api/v1/workspaces/invitations/{workspace_invitation.id}/reject/",
    )

    assert response.status_code == 200
    assert response.data["message"] == "Invitation rejected successfully."
    assert response.data["workspace"] == workspace_invitation.workspace.id
    assert response.data["status"] == InvitationStatus.REJECTED

    workspace_invitation.refresh_from_db()

    assert workspace_invitation.status == InvitationStatus.REJECTED


@pytest.mark.django_db
def test_cancel_invitation(
    client,
    user,
    workspace_invitation,
):
    login_response = client.post(
        "/api/v1/auth/login/",
        {
            "email": user.email,
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert login_response.status_code == 200
    access = login_response.data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
    )
    response = client.post(
        f"/api/v1/workspaces/invitations/{workspace_invitation.id}/cancel/",
    )

    assert response.status_code == 200
    assert response.data["message"] == "Invitation cancelled successfully."
    assert response.data["workspace"] == workspace_invitation.workspace.id
    assert response.data["status"] == InvitationStatus.CANCELLED

    workspace_invitation.refresh_from_db()

    assert workspace_invitation.status == InvitationStatus.CANCELLED


@pytest.mark.django_db
def test_get_workspace_member(
    client,
    user,
    workspace,
    membership,
):
    login_response = client.post(
        "/api/v1/auth/login/",
        {
            "email": user.email,
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert login_response.status_code == 200
    access = login_response.data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
    )
    response = client.get(
        f"/api/v1/workspaces/{workspace.id}/members/{membership.id}/",
    )

    assert response.status_code == 200
    data = response.data["data"]
    assert data["id"] == membership.id
    assert data["email"] == membership.user.email
    assert data["role"] == membership.role


@pytest.mark.django_db
def test_list_membership(
    client,
    user,
    workspace,
    membership,
):
    login_response = client.post(
        "/api/v1/auth/login/",
        {
            "email": user.email,
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert login_response.status_code == 200
    access = login_response.data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
    )
    response = client.get(
        f"/api/v1/workspaces/{workspace.id}/members/",
    )

    assert response.status_code == 200

    data = response.data["data"]

    assert len(data) == 1

    member = data[0]

    assert member["id"] == membership.id
    assert member["email"] == membership.user.email
    assert member["role"] == membership.role


@pytest.mark.django_db
def test_update_member(
    client,
    user,
    workspace,
    membership,
):
    login_response = client.post(
        "/api/v1/auth/login/",
        {
            "email": user.email,
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert login_response.status_code == 200
    access = login_response.data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
    )
    response = client.patch(
        f"/api/v1/workspaces/{workspace.id}/members/{membership.id}/role/",
        {
            "role": "admin",
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["message"] == "Member updated successfully."

    data = response.data["data"]

    assert data["id"] == membership.id
    assert data["email"] == membership.user.email
    assert data["role"] == Role.ADMIN
    assert "joined_at" in data

    membership.refresh_from_db()

    assert membership.role == Role.ADMIN


@pytest.mark.django_db
def test_delete_member(
    client,
    user,
    workspace,
    membership,
):
    login_response = client.post(
        "/api/v1/auth/login/",
        {
            "email": user.email,
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert login_response.status_code == 200
    access = login_response.data["access"]

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
    )
    response = client.delete(
        f"/api/v1/workspaces/{workspace.id}/members/{membership.id}/",
    )

    assert response.status_code == 200
    assert response.data["message"] == f"{membership.user.email} successfully removed from the workspace."
    assert response.data["workspace"] == membership.workspace.id

    assert not Membership.objects.filter(id=membership.id).exists()