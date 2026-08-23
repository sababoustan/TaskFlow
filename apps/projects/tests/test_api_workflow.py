import pytest
from rest_framework import status

from apps.workspaces.choices import Role
from apps.projects.models import Workflow


WORKFLOW_URL = "/api/v1/projects/{}/workflows/"
WORKFLOW_DETAIL_URL = "/api/v1/projects/{}/workflows/{}/"


@pytest.mark.django_db
class TestWorkflowAPI:

    def test_list_workflows_requires_authentication(
        self,
        api_client,
        workspace,
    ):
        url = WORKFLOW_URL.format(workspace.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "role",
        [
            Role.ADMIN,
            Role.MANAGER,
            Role.MEMBER,
            Role.VIEWER,
        ],
    )
    def test_workspace_roles_can_list_workflows(
        self,
        api_client,
        another_user,
        workspace,
        membership_factory,
        workflow,
        role,
    ):
        membership_factory(role)

        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_URL.format(workspace.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1

    def test_workspace_owner_can_list_workflows(
        self,
        authenticated_client,
        workspace,
        workflow,
    ):
        url = WORKFLOW_URL.format(workspace.id)

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1

    def test_user_cannot_list_another_workspace_workflows(
        self,
        authenticated_client,
        another_workspace,
    ):
        url = WORKFLOW_URL.format(another_workspace.id)

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

    @pytest.mark.parametrize(
        "role, expected_status",
        [
            (Role.ADMIN, status.HTTP_201_CREATED),
            (Role.MANAGER, status.HTTP_201_CREATED),
            (Role.MEMBER, status.HTTP_403_FORBIDDEN),
            (Role.VIEWER, status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_workflow_by_role(
        self,
        api_client,
        another_user,
        workspace,
        membership_factory,
        role,
        expected_status,
    ):
        membership_factory(role)

        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_URL.format(workspace.id)

        response = api_client.post(
            url,
            {"name": "Development"},
            format="json",
        )

        assert response.status_code == expected_status

    def test_owner_can_create_workflow(
        self,
        authenticated_client,
        workspace,
    ):
        url = WORKFLOW_URL.format(workspace.id)

        response = authenticated_client.post(
            url,
            {"name": "Development"},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert Workflow.objects.filter(
            workspace=workspace,
            name="Development",
        ).exists()

    def test_unauthenticated_user_cannot_create_workflow(
        self,
        api_client,
        workspace,
    ):
        url = WORKFLOW_URL.format(workspace.id)

        response = api_client.post(
            url,
            {"name": "Development"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_create_duplicate_workflow(
        self,
        authenticated_client,
        workspace,
        workflow,
    ):
        url = WORKFLOW_URL.format(workspace.id)

        response = authenticated_client.post(
            url,
            {"name": workflow.name},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == (
            "This workflow already exists."
        )

        assert Workflow.objects.filter(
            workspace=workspace,
            name=workflow.name,
        ).count() == 1

    def test_cannot_create_workflow_without_name(
        self,
        authenticated_client,
        workspace,
    ):
        url = WORKFLOW_URL.format(workspace.id)

        response = authenticated_client.post(
            url,
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_cannot_create_workflow_with_name_longer_than_100_characters(
        self,
        authenticated_client,
        workspace,
    ):
        url = WORKFLOW_URL.format(workspace.id)

        response = authenticated_client.post(
            url,
            {"name": "A" * 101},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    @pytest.mark.parametrize(
        "role, expected_status",
        [
            (Role.ADMIN, status.HTTP_200_OK),
            (Role.MANAGER, status.HTTP_200_OK),
            (Role.MEMBER, status.HTTP_403_FORBIDDEN),
            (Role.VIEWER, status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_update_workflow_by_role(
        self,
        api_client,
        another_user,
        workspace,
        membership_factory,
        workflow,
        role,
        expected_status,
    ):
        membership_factory(role)

        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_DETAIL_URL.format(
            workspace.id,
            workflow.id,
        )

        response = api_client.patch(
            url,
            {"name": "Production"},
            format="json",
        )

        assert response.status_code == expected_status

        workflow.refresh_from_db()

        if expected_status == status.HTTP_200_OK:
            assert workflow.name == "Production"
        else:
            assert workflow.name == "Development"

    def test_owner_can_update_workflow(
        self,
        authenticated_client,
        workspace,
        workflow,
    ):
        url = WORKFLOW_DETAIL_URL.format(
            workspace.id,
            workflow.id,
        )

        response = authenticated_client.patch(
            url,
            {"name": "Production"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        workflow.refresh_from_db()

        assert workflow.name == "Production"

    def test_unauthenticated_user_cannot_update_workflow(
        self,
        api_client,
        workspace,
        workflow,
    ):
        url = WORKFLOW_DETAIL_URL.format(
            workspace.id,
            workflow.id,
        )

        response = api_client.patch(
            url,
            {"name": "Production"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_update_workflow_to_duplicate_name(
        self,
        authenticated_client,
        workspace,
        workflow,
        workflow_same_workspace,
    ):
        url = WORKFLOW_DETAIL_URL.format(
            workspace.id,
            workflow.id,
        )

        response = authenticated_client.patch(
            url,
            {"name": workflow_same_workspace.name},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == (
            "This workflow already exists."
        )

        workflow.refresh_from_db()

        assert workflow.name == "Development"

    def test_cannot_update_workflow_without_name(
        self,
        authenticated_client,
        workspace,
        workflow,
    ):
        url = WORKFLOW_DETAIL_URL.format(
            workspace.id,
            workflow.id,
        )

        response = authenticated_client.patch(
            url,
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_update_workflow_in_wrong_workspace_returns_404(
        self,
        authenticated_client,
        workspace,
        workflow_another,
    ):
        url = WORKFLOW_DETAIL_URL.format(
            workspace.id,
            workflow_another.id,
        )

        response = authenticated_client.patch(
            url,
            {"name": "Production"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.parametrize(
        "role, expected_status",
        [
            (Role.ADMIN, status.HTTP_204_NO_CONTENT),
            (Role.MANAGER, status.HTTP_403_FORBIDDEN),
            (Role.MEMBER, status.HTTP_403_FORBIDDEN),
            (Role.VIEWER, status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_delete_workflow(
        self,
        api_client,
        workspace,
        membership_factory,
        workflow,
        role,
        expected_status,
        another_user,
    ):
        membership_factory(role)

        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_DETAIL_URL.format(
            workspace.id,
            workflow.id,
        )

        response = api_client.delete(url)

        assert response.status_code == expected_status

        if expected_status == status.HTTP_204_NO_CONTENT:
            assert not Workflow.objects.filter(
                id=workflow.id
            ).exists()
        else:
            assert Workflow.objects.filter(
                id=workflow.id
            ).exists()

    def test_owner_can_delete_workflow(
        self,
        authenticated_client,
        workspace,
        workflow,
    ):
        url = WORKFLOW_DETAIL_URL.format(
            workspace.id,
            workflow.id,
        )

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Workflow.objects.filter(
            id=workflow.id
        ).exists()

    def test_unauthenticated_user_cannot_delete_workflow(
        self,
        api_client,
        workspace,
        workflow,
    ):
        url = WORKFLOW_DETAIL_URL.format(
            workspace.id,
            workflow.id,
        )

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_nonexistent_workflow(
        self,
        authenticated_client,
        workspace,
    ):
        url = WORKFLOW_DETAIL_URL.format(
            workspace.id,
            99999,
        )

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cannot_delete_workflow_with_project(
        self,
        authenticated_client,
        workspace,
        workflow,
        project,
    ):
        url = WORKFLOW_DETAIL_URL.format(
            workspace.id,
            workflow.id,
        )

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == (
            "This workflow is project-dependent and cannot be deleted."
        )

        assert Workflow.objects.filter(
            id=workflow.id
        ).exists()