import pytest
from rest_framework import status

from apps.workspaces.choices import (
    InvitationStatus,
    Role,
)
from apps.workspaces.models import Membership, WorkspaceInvitation, Workspace


WORKSPACE_URL = "/api/v1/workspaces/"
WORKSPACE_DETAIL_URL = "/api/v1/workspaces/{}/"


@pytest.mark.django_db
class TestWorkspaceAPI:

    def test_list_workspaces_requires_authentication(
        self,
        api_client,
    ):
        response = api_client.get(WORKSPACE_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_can_list_owned_workspaces(
        self,
        authenticated_client,
        workspace,
    ):
        response = authenticated_client.get(WORKSPACE_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == workspace.id
        assert response.data[0]["title"] == workspace.title

    def test_member_can_list_workspace(
        self,
        api_client,
        invited_user,
        workspace,
        membership,
    ):
        api_client.force_authenticate(user=invited_user)

        response = api_client.get(WORKSPACE_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["id"] == workspace.id

    def test_user_cannot_list_workspace_they_are_not_member_of(
        self,
        api_client,
        unrelated_user,
        another_workspace,
    ):
        api_client.force_authenticate(user=unrelated_user)

        response = api_client.get(WORKSPACE_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_user_can_create_workspace(
        self,
        authenticated_client,
        user,
    ):
        response = authenticated_client.post(
            WORKSPACE_URL,
            {
                "title": "Django Project",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        workspace = Workspace.objects.get(
            title="Django Project",
        )

        assert workspace.owner == user
        assert workspace.title == "Django Project"
        assert workspace.slug == "django-project"

    def test_unauthenticated_user_cannot_create_workspace(
        self,
        api_client,
    ):
        response = api_client.post(
            WORKSPACE_URL,
            {"title": "Django Project"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Workspace.objects.count() == 0

    def test_user_cannot_create_workspace_without_title(
        self,
        authenticated_client,
    ):
        response = authenticated_client.post(
            WORKSPACE_URL,
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data
        assert Workspace.objects.count() == 0

    def test_user_cannot_create_workspace_with_empty_title(
        self,
        authenticated_client,
    ):
        response = authenticated_client.post(
            WORKSPACE_URL,
            {
                "title": "",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data
        assert Workspace.objects.count() == 0

    def test_user_can_retrieve_owned_workspace(
        self,
        authenticated_client,
        workspace,
    ):
        url = WORKSPACE_DETAIL_URL.format(workspace.id)

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == workspace.id
        assert response.data["title"] == workspace.title

    def test_member_can_retrieve_workspace(
        self,
        api_client,
        invited_user,
        workspace,
        membership,
    ):
        api_client.force_authenticate(user=invited_user)

        url = WORKSPACE_DETAIL_URL.format(workspace.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == workspace.id

    def test_user_cannot_retrieve_unaccessible_workspace(
        self,
        api_client,
        unrelated_user,
        another_workspace,
    ):
        api_client.force_authenticate(user=unrelated_user)

        url = WORKSPACE_DETAIL_URL.format(another_workspace.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_owner_can_update_workspace(
        self,
        authenticated_client,
        workspace,
    ):
        url = WORKSPACE_DETAIL_URL.format(workspace.id)

        response = authenticated_client.patch(
            url,
            {
                "title": "Updated Workspace",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        workspace.refresh_from_db()

        assert workspace.title == "Updated Workspace"

    def test_owner_cannot_update_workspace_with_empty_title(
        self,
        authenticated_client,
        workspace,
    ):
        url = WORKSPACE_DETAIL_URL.format(workspace.id)

        response = authenticated_client.patch(
            url,
            {"title": ""},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

        workspace.refresh_from_db()

        assert workspace.title != ""

    def test_user_cannot_update_another_workspace(
        self,
        authenticated_client,
        another_workspace,
    ):
        url = WORKSPACE_DETAIL_URL.format(another_workspace.id)

        response = authenticated_client.patch(
            url,
            {"title": "Hacked Workspace"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        "role",
        [
            Role.MANAGER,
            Role.MEMBER,
            Role.VIEWER,
        ],
    )
    def test_non_owner_cannot_update_workspace(
        self,
        api_client,
        invited_user,
        workspace,
        membership,
        role,
    ):
        membership.role = role
        membership.save(update_fields=["role"])

        api_client.force_authenticate(user=invited_user)

        url = WORKSPACE_DETAIL_URL.format(workspace.id)

        response = api_client.patch(
            url,
            {"title": "Hacked Workspace"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_owner_can_delete_workspace(
        self,
        authenticated_client,
        workspace,
    ):
        url = WORKSPACE_DETAIL_URL.format(workspace.id)

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Workspace.objects.filter(id=workspace.id).exists()

    def test_member_cannot_delete_workspace(
        self,
        api_client,
        invited_user,
        workspace,
        membership,
    ):
        api_client.force_authenticate(user=invited_user)

        url = WORKSPACE_DETAIL_URL.format(workspace.id)

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Workspace.objects.filter(id=workspace.id).exists()

    def test_user_cannot_delete_another_workspace(
        self,
        authenticated_client,
        another_workspace,
    ):
        url = WORKSPACE_DETAIL_URL.format(another_workspace.id)

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Workspace.objects.filter(
            id=another_workspace.id
        ).exists()


INVITATION_URL = "/api/v1/workspaces/{}/invitations/"
ACCEPT_INVITATION_URL = "/api/v1/workspaces/invitations/{}/accept/"
REJECT_INVITATION_URL = "/api/v1/workspaces/invitations/{}/reject/"
CANCEL_INVITATION_URL = "/api/v1/workspaces/invitations/{}/cancel/"


@pytest.mark.django_db
class TestInvitationAPI:

    def test_unauthenticated_user_cannot_create_invitation(
        self,
        api_client,
        workspace,
        invited_user,
    ):
        url = INVITATION_URL.format(workspace.id)

        response = api_client.post(
            url,
            {
                "email": invited_user.email,
                "role": Role.MEMBER,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "role",
        [
            Role.MANAGER,
            Role.MEMBER,
            Role.VIEWER,
        ],
    )
    def test_non_admin_cannot_create_invitation(
        self,
        api_client,
        invited_user,
        workspace,
        membership,
        role,
    ):
        membership.role = role
        membership.save(update_fields=["role"])

        api_client.force_authenticate(user=invited_user)

        url = INVITATION_URL.format(workspace.id)

        response = api_client.post(
            url,
            {
                "email": "newuser@gmail.com",
                "role": Role.MEMBER,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_invitations(
        self,
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

        url = INVITATION_URL.format(workspace.id)

        response = client.get(url)

        assert response.status_code == 200

        invitation = response.data["data"][0]

        assert invitation["id"] == workspace_invitation.id
        assert invitation["email"] == workspace_invitation.user.email
        assert invitation["invited_by"] == (
            workspace_invitation.invited_by.email
        )
        assert invitation["role"] == workspace_invitation.role
        assert invitation["status"] == workspace_invitation.status

    def test_cannot_create_duplicate_pending_invitation(
        self,
        authenticated_client,
        workspace,
        workspace_invitation,
    ):
        url = INVITATION_URL.format(workspace.id)

        response = authenticated_client.post(
            url,
            {
                "email": workspace_invitation.user.email,
                "role": Role.MEMBER,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_accept_invitation(
        self,
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

        url = ACCEPT_INVITATION_URL.format(
            workspace_invitation.id
        )

        response = client.post(url)

        assert response.status_code == 201
        assert response.data["message"] == (
            "Invitation accepted successfully."
        )
        assert response.data["workspace"] == workspace.id

        membership = Membership.objects.get(
            workspace=workspace,
            user=invited_user,
        )

        assert membership.workspace == workspace
        assert membership.user == invited_user
        assert membership.role == Role.MEMBER

        workspace_invitation.refresh_from_db()

        assert workspace_invitation.status == (
            InvitationStatus.ACCEPTED
        )

    def test_user_cannot_accept_another_users_invitation(
        self,
        api_client,
        user,
        workspace_invitation,
    ):
        api_client.force_authenticate(user=user)

        url = ACCEPT_INVITATION_URL.format(
            workspace_invitation.id
        )

        response = api_client.post(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_reject_invitation(
        self,
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

        url = REJECT_INVITATION_URL.format(
            workspace_invitation.id
        )

        response = client.post(url)

        assert response.status_code == 200
        assert response.data["message"] == (
            "Invitation rejected successfully."
        )
        assert response.data["workspace"] == (
            workspace_invitation.workspace.id
        )
        assert response.data["status"] == (
            InvitationStatus.REJECTED
        )

        workspace_invitation.refresh_from_db()

        assert workspace_invitation.status == (
            InvitationStatus.REJECTED
        )

    def test_user_cannot_reject_another_users_invitation(
        self,
        api_client,
        user,
        workspace_invitation,
    ):
        api_client.force_authenticate(user=user)

        url = REJECT_INVITATION_URL.format(
            workspace_invitation.id
        )

        response = api_client.post(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_cancel_invitation(
        self,
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

        url = CANCEL_INVITATION_URL.format(
            workspace_invitation.id
        )

        response = client.post(url)

        assert response.status_code == 200
        assert response.data["message"] == (
            "Invitation cancelled successfully."
        )
        assert response.data["workspace"] == (
            workspace_invitation.workspace.id
        )
        assert response.data["status"] == (
            InvitationStatus.CANCELLED
        )

        workspace_invitation.refresh_from_db()

        assert workspace_invitation.status == (
            InvitationStatus.CANCELLED
        )

    @pytest.mark.parametrize(
        "role",
        [
            Role.MANAGER,
            Role.MEMBER,
            Role.VIEWER,
        ],
    )
    def test_non_admin_cannot_cancel_invitation(
        self,
        api_client,
        invited_user,
        workspace,
        workspace_invitation,
        membership,
        role,
    ):
        membership.role = role
        membership.save(update_fields=["role"])

        api_client.force_authenticate(user=invited_user)

        url = CANCEL_INVITATION_URL.format(
            workspace_invitation.id
        )

        response = api_client.post(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN


MEMBERSHIP_URL = "/api/v1/workspaces/{}/members/"
MEMBERSHIP_DETAIL_URL = "/api/v1/workspaces/{}/members/{}/"
MEMBERSHIP_ROLE_URL = "/api/v1/workspaces/{}/members/{}/role/"


@pytest.mark.django_db
class TestMembershipAPI:

    def test_get_workspace_member(
        self,
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

        url = MEMBERSHIP_DETAIL_URL.format(
            workspace.id,
            membership.id,
        )

        response = client.get(url)

        assert response.status_code == 200

        data = response.data["data"]

        assert data["id"] == membership.id
        assert data["email"] == membership.user.email
        assert data["role"] == membership.role
        assert "joined_at" in data

    def test_list_membership(
        self,
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

        url = MEMBERSHIP_URL.format(workspace.id)

        response = client.get(url)

        assert response.status_code == 200

        data = response.data["data"]

        assert len(data) == 1

        member = data[0]

        assert member["id"] == membership.id
        assert member["email"] == membership.user.email
        assert member["role"] == membership.role
        assert "joined_at" in member

    def test_update_member(
        self,
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

        url = MEMBERSHIP_ROLE_URL.format(
            workspace.id,
            membership.id,
        )

        response = client.patch(
            url,
            {
                "role": Role.ADMIN,
            },
            format="json",
        )

        assert response.status_code == 200
        assert response.data["message"] == (
            "Member updated successfully."
        )

        data = response.data["data"]

        assert data["id"] == membership.id
        assert data["email"] == membership.user.email
        assert data["role"] == Role.ADMIN
        assert "joined_at" in data

        membership.refresh_from_db()

        assert membership.role == Role.ADMIN

    def test_delete_member(
        self,
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

        url = MEMBERSHIP_DETAIL_URL.format(
            workspace.id,
            membership.id,
        )

        response = client.delete(url)

        assert response.status_code == 200

        assert response.data["message"] == (
            f"{membership.user.email} "
            "successfully removed from the workspace."
        )

        assert response.data["workspace"] == membership.workspace.id

        assert not Membership.objects.filter(
            id=membership.id
        ).exists()