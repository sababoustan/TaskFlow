import pytest
from rest_framework import status

from apps.projects.models import Project
from apps.workspaces.models import Role


PROJECT_URL = "/api/v1/projects/{}/projects/"
PROJECT_CREATE_URL = "/api/v1/projects/{}/workflows/{}/projects/"
PROJECT_UPDATE_URL = "/api/v1/projects/{}/projects/{}/"


@pytest.mark.django_db
class TestProjectAPI:

    def test_list_project_requires_authentication(
        self,
        api_client,
        workspace,
    ):
        url = PROJECT_URL.format(workspace.id)

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
    def test_workspace_roles_can_list_projects(
        self,
        api_client,
        another_user,
        workspace,
        membership_factory,
        project,
        role,
    ):
        membership_factory(role)

        api_client.force_authenticate(user=another_user)

        url = PROJECT_URL.format(workspace.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1

    def test_owner_can_list_projects(
        self,
        authenticated_client,
        workspace,
        project,
    ):
        url = PROJECT_URL.format(workspace.id)

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1

    def test_user_cannot_list_projects_from_another_workspace(
        self,
        authenticated_client,
        another_workspace,
    ):
        url = PROJECT_URL.format(another_workspace.id)

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

    def test_unauthenticated_user_cannot_create_project(
        self,
        api_client,
        workspace,
        workflow,
    ):
        url = PROJECT_CREATE_URL.format(
            workspace.id,
            workflow.id,
        )

        response = api_client.post(
            url,
            {"name": "E-commerce Platform"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "role",
        [
            Role.ADMIN,
            Role.MANAGER,
        ],
    )
    def test_admin_and_manager_can_create_project(
        self,
        api_client,
        another_user,
        workspace,
        workflow,
        membership_factory,
        role,
    ):
        membership_factory(role)

        api_client.force_authenticate(user=another_user)

        url = PROJECT_CREATE_URL.format(
            workspace.id,
            workflow.id,
        )

        response = api_client.post(
            url,
            {
                "name": "E-commerce Platform",
                "description": (
                    "Develop the backend and API "
                    "for the e-commerce platform."
                ),
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert Project.objects.filter(
            workspace=workspace,
            workflow=workflow,
            name="E-commerce Platform",
        ).exists()

    @pytest.mark.parametrize(
        "role",
        [
            Role.MEMBER,
            Role.VIEWER,
        ],
    )
    def test_member_and_viewer_cannot_create_project(
        self,
        api_client,
        another_user,
        workspace,
        workflow,
        membership_factory,
        role,
    ):
        membership_factory(role)

        api_client.force_authenticate(user=another_user)

        url = PROJECT_CREATE_URL.format(
            workspace.id,
            workflow.id,
        )

        response = api_client.post(
            url,
            {"name": "E-commerce Platform"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

    def test_owner_can_create_project(
        self,
        authenticated_client,
        workspace,
        workflow,
    ):
        url = PROJECT_CREATE_URL.format(
            workspace.id,
            workflow.id,
        )

        response = authenticated_client.post(
            url,
            {
                "name": "E-commerce Platform",
                "description": (
                    "Develop the backend and API "
                    "for the e-commerce platform."
                ),
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert Project.objects.filter(
            workspace=workspace,
            workflow=workflow,
            name="E-commerce Platform",
        ).exists()

    def test_cannot_create_project_without_name(
        self,
        authenticated_client,
        workspace,
        workflow,
    ):
        url = PROJECT_CREATE_URL.format(
            workspace.id,
            workflow.id,
        )

        response = authenticated_client.post(
            url,
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_cannot_create_project_with_name_longer_than_255_characters(
        self,
        authenticated_client,
        workspace,
        workflow,
    ):
        url = PROJECT_CREATE_URL.format(
            workspace.id,
            workflow.id,
        )

        response = authenticated_client.post(
            url,
            {"name": "A" * 256},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_cannot_create_project_with_description_longer_than_255_characters(
        self,
        authenticated_client,
        workspace,
        workflow,
    ):
        url = PROJECT_CREATE_URL.format(
            workspace.id,
            workflow.id,
        )

        response = authenticated_client.post(
            url,
            {
                "name": "E-commerce Platform",
                "description": "A" * 256,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "description" in response.data

    def test_cannot_create_project_with_workflow_from_another_workspace(
        self,
        authenticated_client,
        workspace,
        workflow_another,
    ):
        url = PROJECT_CREATE_URL.format(
            workspace.id,
            workflow_another.id,
        )

        response = authenticated_client.post(
            url,
            {"name": "E-commerce Platform"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_project_requires_authentication(
        self,
        api_client,
        workspace,
        project,
    ):
        url = PROJECT_UPDATE_URL.format(
            workspace.id,
            project.id,
        )

        response = api_client.patch(
            url,
            {"name": "Production"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "role, expected_status",
        [
            (Role.ADMIN, status.HTTP_200_OK),
            (Role.MANAGER, status.HTTP_200_OK),
            (Role.MEMBER, status.HTTP_403_FORBIDDEN),
            (Role.VIEWER, status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_update_project_by_role(
        self,
        api_client,
        another_user,
        workspace,
        membership_factory,
        project,
        role,
        expected_status,
    ):
        membership_factory(role)

        api_client.force_authenticate(user=another_user)

        url = PROJECT_UPDATE_URL.format(
            workspace.id,
            project.id,
        )

        response = api_client.patch(
            url,
            {"name": "Production"},
            format="json",
        )

        assert response.status_code == expected_status

        project.refresh_from_db()

        if expected_status == status.HTTP_200_OK:
            assert project.name == "Production"
        else:
            assert project.name == "E-commerce Platform"

    def test_owner_can_update_project(
        self,
        authenticated_client,
        workspace,
        project,
    ):
        url = PROJECT_UPDATE_URL.format(
            workspace.id,
            project.id,
        )

        response = authenticated_client.patch(
            url,
            {"name": "Production"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        project.refresh_from_db()

        assert project.name == "Production"

    def test_user_cannot_update_project_from_another_workspace(
        self,
        authenticated_client,
        another_workspace,
        another_project,
    ):
        url = PROJECT_UPDATE_URL.format(
            another_workspace.id,
            another_project.id,
        )

        response = authenticated_client.patch(
            url,
            {"name": "Production"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

    def test_update_nonexistent_project(
        self,
        authenticated_client,
        workspace,
    ):
        url = PROJECT_UPDATE_URL.format(
            workspace.id,
            99999,
        )

        response = authenticated_client.patch(
            url,
            {"name": "Production"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND