import pytest
from rest_framework import status

from apps.projects.models import Sprint


SPRINT_URL = "/api/v1/projects/workspaces/{}/projects/{}/sprints/"
SPRINT_DETAIL_URL = (
    "/api/v1/projects/workspaces/{}/projects/{}/sprints/{}/"
)


@pytest.mark.django_db
class TestSprintAPI:

    def test_list_sprints_requires_authentication(
        self,
        api_client,
        workspace,
        project,
    ):
        url = SPRINT_URL.format(workspace.id, project.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "role_fixture",
        [
            "workspace_admin",
            "workspace_manager",
            "workspace_member",
            "workspace_viewer",
        ],
    )
    def test_workspace_roles_can_list_sprints(
        self,
        api_client,
        another_user,
        workspace,
        project,
        sprint,
        request,
        role_fixture,
    ):
        request.getfixturevalue(role_fixture)

        api_client.force_authenticate(user=another_user)

        url = SPRINT_URL.format(workspace.id, project.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1

    def test_owner_can_list_sprints(
        self,
        authenticated_client,
        workspace,
        project,
        sprint,
    ):
        url = SPRINT_URL.format(workspace.id, project.id)

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1

    def test_user_cannot_list_sprints_from_another_workspace(
        self,
        authenticated_client,
        another_workspace,
        another_project,
    ):
        url = SPRINT_URL.format(
            another_workspace.id,
            another_project.id,
        )

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

    def test_unauthenticated_user_cannot_create_sprint(
        self,
        api_client,
        workspace,
        project,
    ):
        url = SPRINT_URL.format(workspace.id, project.id)

        response = api_client.post(
            url,
            {"name": "Sprint 1"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "role_fixture",
        [
            "workspace_admin",
            "workspace_manager",
        ],
    )
    def test_admin_and_manager_can_create_sprint(
        self,
        api_client,
        another_user,
        workspace,
        project,
        request,
        role_fixture,
    ):
        request.getfixturevalue(role_fixture)

        api_client.force_authenticate(user=another_user)

        url = SPRINT_URL.format(workspace.id, project.id)

        response = api_client.post(
            url,
            {
                "name": "Sprint 1",
                "start_date": "2026-08-19T08:03:25Z",
                "end_date": "2026-09-19T08:03:25Z",
                "goal": "Complete authentication features.",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        sprint = Sprint.objects.get(
            project=project,
            name="Sprint 1",
        )

        assert sprint.start_date is not None
        assert sprint.end_date is not None
        assert sprint.goal == "Complete authentication features."

    @pytest.mark.parametrize(
        "role_fixture",
        [
            "workspace_member",
            "workspace_viewer",
        ],
    )
    def test_member_and_viewer_cannot_create_sprint(
        self,
        api_client,
        another_user,
        workspace,
        project,
        request,
        role_fixture,
    ):
        request.getfixturevalue(role_fixture)

        api_client.force_authenticate(user=another_user)

        url = SPRINT_URL.format(workspace.id, project.id)

        response = api_client.post(
            url,
            {"name": "Sprint 1"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

    def test_owner_can_create_sprint(
        self,
        authenticated_client,
        workspace,
        project,
    ):
        url = SPRINT_URL.format(workspace.id, project.id)

        response = authenticated_client.post(
            url,
            {
                "name": "Sprint 1",
                "start_date": "2026-08-19T08:03:25Z",
                "end_date": "2026-09-19T08:03:25Z",
                "goal": "Complete authentication features.",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert Sprint.objects.filter(
            project=project,
            name="Sprint 1",
        ).exists()

    def test_cannot_create_duplicate_sprint_name(
        self,
        authenticated_client,
        workspace,
        project,
        sprint,
    ):
        url = SPRINT_URL.format(workspace.id, project.id)

        response = authenticated_client.post(
            url,
            {
                "name": sprint.name,
                "start_date": "2026-09-19T08:03:25Z",
                "end_date": "2026-10-19T08:03:25Z",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["name"] == (
            "A sprint with this name already exists in this project."
        )

    def test_cannot_create_sprint_without_name(
        self,
        authenticated_client,
        workspace,
        project,
    ):
        url = SPRINT_URL.format(workspace.id, project.id)

        response = authenticated_client.post(
            url,
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_cannot_create_sprint_with_name_longer_than_255_characters(
        self,
        authenticated_client,
        workspace,
        project,
    ):
        url = SPRINT_URL.format(workspace.id, project.id)

        response = authenticated_client.post(
            url,
            {"name": "A" * 256},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_cannot_create_sprint_with_goal_longer_than_500_characters(
        self,
        authenticated_client,
        workspace,
        project,
    ):
        url = SPRINT_URL.format(workspace.id, project.id)

        response = authenticated_client.post(
            url,
            {
                "name": "Sprint 1",
                "goal": "A" * 501,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "goal" in response.data

    def test_can_create_sprint_without_optional_fields(
        self,
        authenticated_client,
        workspace,
        project,
    ):
        url = SPRINT_URL.format(workspace.id, project.id)

        response = authenticated_client.post(
            url,
            {"name": "Sprint 1"},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        sprint = Sprint.objects.get(
            project=project,
            name="Sprint 1",
        )

        assert sprint.start_date is None
        assert sprint.end_date is None
        assert sprint.goal == ""

    def test_cannot_create_sprint_with_end_date_before_start_date(
        self,
        authenticated_client,
        workspace,
        project,
    ):
        url = SPRINT_URL.format(workspace.id, project.id)

        response = authenticated_client.post(
            url,
            {
                "name": "Sprint 1",
                "start_date": "2026-09-20T10:00:00Z",
                "end_date": "2026-09-19T10:00:00Z",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "end_date" in response.data
        assert response.data["end_date"][0] == (
            "End date must be after start date."
        )

    def test_unauthenticated_user_cannot_update_sprint(
        self,
        api_client,
        workspace,
        project,
        sprint,
    ):
        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            sprint.id,
        )

        response = api_client.patch(
            url,
            {"name": "Sprint 2"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_can_update_sprint(
        self,
        api_client,
        another_user,
        workspace,
        project,
        sprint,
        workspace_admin,
    ):
        api_client.force_authenticate(user=another_user)

        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            sprint.id,
        )

        response = api_client.patch(
            url,
            {"name": "Sprint 2"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        sprint.refresh_from_db()

        assert sprint.name == "Sprint 2"

    def test_manager_can_update_sprint(
        self,
        api_client,
        another_user,
        workspace,
        project,
        sprint,
        workspace_manager,
    ):
        api_client.force_authenticate(user=another_user)

        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            sprint.id,
        )

        response = api_client.patch(
            url,
            {"name": "Sprint 2"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        sprint.refresh_from_db()

        assert sprint.name == "Sprint 2"

    @pytest.mark.parametrize(
        "role_fixture",
        [
            "workspace_member",
            "workspace_viewer",
        ],
    )
    def test_member_and_viewer_cannot_update_sprint(
        self,
        api_client,
        another_user,
        workspace,
        project,
        sprint,
        request,
        role_fixture,
    ):
        request.getfixturevalue(role_fixture)

        api_client.force_authenticate(user=another_user)

        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            sprint.id,
        )

        response = api_client.patch(
            url,
            {"name": "Sprint 2"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

        sprint.refresh_from_db()

        assert sprint.name == "Sprint 1"

    def test_cannot_update_sprint_to_duplicate_name(
        self,
        authenticated_client,
        workspace,
        project,
        sprint,
        sprint_another,
    ):
        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            sprint.id,
        )

        response = authenticated_client.patch(
            url,
            {"name": sprint_another.name},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cannot_update_sprint_with_end_date_before_start_date(
        self,
        authenticated_client,
        workspace,
        project,
        sprint,
    ):
        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            sprint.id,
        )

        response = authenticated_client.patch(
            url,
            {
                "start_date": "2026-09-20T10:00:00Z",
                "end_date": "2026-09-19T10:00:00Z",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "end_date" in response.data

    def test_update_nonexistent_sprint(
        self,
        authenticated_client,
        workspace,
        project,
    ):
        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            99999,
        )

        response = authenticated_client.patch(
            url,
            {"name": "Sprint 2"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_unauthenticated_user_cannot_delete_sprint(
        self,
        api_client,
        workspace,
        project,
        sprint,
    ):
        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            sprint.id,
        )

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_owner_can_delete_sprint(
        self,
        authenticated_client,
        workspace,
        project,
        sprint,
    ):
        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            sprint.id,
        )

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Sprint.objects.filter(
            id=sprint.id
        ).exists()

    def test_admin_can_delete_sprint(
        self,
        api_client,
        another_user,
        workspace,
        project,
        sprint,
        workspace_admin,
    ):
        api_client.force_authenticate(user=another_user)

        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            sprint.id,
        )

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Sprint.objects.filter(
            id=sprint.id
        ).exists()

    @pytest.mark.parametrize(
        "role_fixture",
        [
            "workspace_manager",
            "workspace_member",
            "workspace_viewer",
        ],
    )
    def test_manager_member_and_viewer_cannot_delete_sprint(
        self,
        api_client,
        another_user,
        workspace,
        project,
        sprint,
        request,
        role_fixture,
    ):
        request.getfixturevalue(role_fixture)

        api_client.force_authenticate(user=another_user)

        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            sprint.id,
        )

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert Sprint.objects.filter(
            id=sprint.id
        ).exists()

    def test_delete_nonexistent_sprint(
        self,
        authenticated_client,
        workspace,
        project,
    ):
        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            99999,
        )

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND