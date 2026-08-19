import pytest
from rest_framework import status
from apps.projects.models import Project, Status, Workflow, WorkflowStatus, Sprint

STATUS_URL = "/api/v1/projects/statuses/"


@pytest.mark.django_db
class TestStatusAPI:
    def test_list_status_requires_authentication(
        self,
        api_client,
        status_obj,
    ):
        response = api_client.get(STATUS_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_status_authenticated_user(
        self,
        authenticated_client,
        status_obj,
    ):
        response = authenticated_client.get(STATUS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_admin_can_create_status(
        self,
        admin_client,
    ):
        response = admin_client.post(
            STATUS_URL,
            {"name": "In Progress"},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert Status.objects.filter(name="In Progress").exists()

    def test_normal_user_cannot_create_status(
        self,
        authenticated_client,
    ):
        response = authenticated_client.post(
            STATUS_URL,
            {"name": "In Progress"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_update_status(
        self,
        admin_client,
        status_obj,
    ):
        url = f"{STATUS_URL}{status_obj.id}/"

        response = admin_client.patch(
            url,
            {"name": "Done"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        status_obj.refresh_from_db()

        assert status_obj.name == "Done"

    def test_normal_user_cannot_update_status(
        self,
        authenticated_client,
        status_obj,
    ):
        url = f"{STATUS_URL}{status_obj.id}/"

        response = authenticated_client.patch(
            url,
            {"name": "Done"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_delete_status(
        self,
        admin_client,
        status_obj,
    ):
        url = f"{STATUS_URL}{status_obj.id}/"

        response = admin_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Status.objects.filter(id=status_obj.id).exists()

    def test_normal_user_cannot_delete_status(
        self,
        authenticated_client,
        status_obj,
    ):
        url = f"{STATUS_URL}{status_obj.id}/"

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Status.objects.filter(id=status_obj.id).exists()


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

    def test_workspace_member_can_list_workflows(
        self,
        api_client,
        another_user,
        workspace,
        workspace_member,
        workflow,
    ):
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

    def test_admin_can_create_workflow(
        self,
        api_client,
        another_user,
        workspace,
        workspace_admin,
    ):
        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_URL.format(workspace.id)

        response = api_client.post(
            url,
            {"name": "Development"},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert Workflow.objects.filter(
            workspace=workspace,
            name="Development",
        ).exists()

    def test_manager_can_create_workflow(
        self,
        api_client,
        another_user,
        workspace,
        workspace_manager,
    ):
        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_URL.format(workspace.id)

        response = api_client.post(
            url,
            {"name": "Development"},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_member_cannot_create_workflow(
        self,
        api_client,
        another_user,
        workspace,
        workspace_member,
    ):
        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_URL.format(workspace.id)

        response = api_client.post(
            url,
            {"name": "Development"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

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

    def test_update_workflow(
        self,
        api_client,
        another_user,
        workspace,
        workspace_admin,
        workflow,
    ):
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

        assert response.status_code == status.HTTP_200_OK

        workflow.refresh_from_db()

        assert workflow.name == "Production"

    def test_member_cannot_update_workflow(
        self,
        api_client,
        another_user,
        workspace,
        workspace_member,
        workflow,
    ):
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

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

        workflow.refresh_from_db()

        assert workflow.name == "Development"

    def test_manager_can_update_workflow(
        self,
        api_client,
        another_user,
        workspace,
        workspace_manager,
        workflow,
    ):
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

        assert response.status_code == status.HTTP_200_OK

        workflow.refresh_from_db()

        assert workflow.name == "Production"

    def test_delete_workflow(
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

        assert response.status_code == status.HTTP_200_OK

        assert not Workflow.objects.filter(id=workflow.id).exists()

    def test_member_cannot_delete_workflow(
        self,
        api_client,
        another_user,
        workspace,
        workspace_member,
        workflow,
    ):
        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_DETAIL_URL.format(
            workspace.id,
            workflow.id,
        )

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

        assert Workflow.objects.filter(id=workflow.id).exists()

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

    def test_member_can_list_project(
        self,
        api_client,
        another_user,
        workspace,
        workspace_member,
        project,
    ):
        api_client.force_authenticate(user=another_user)

        url = PROJECT_URL.format(workspace.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1

    def test_user_cannot_list_another_project(
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

    def test_admin_can_create_project(
        self, api_client, another_user, workspace, workflow, workspace_admin
    ):
        api_client.force_authenticate(user=another_user)

        url = PROJECT_CREATE_URL.format(workspace.id, workflow.id)

        response = api_client.post(
            url,
            {
                "name": "E-commerce Platform",
                "description": "Develop the backend and API for the e-commerce platform.",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert Project.objects.filter(
            workspace=workspace,
            workflow=workflow,
            name="E-commerce Platform",
            description="Develop the backend and API for the e-commerce platform.",
        ).exists()

    def test_manager_can_create_project(
        self, api_client, another_user, workspace, workspace_manager, workflow
    ):
        api_client.force_authenticate(user=another_user)

        url = PROJECT_CREATE_URL.format(workspace.id, workflow.id)

        response = api_client.post(
            url,
            {
                "name": "E-commerce Platform",
                "description": "Develop the backend and API for the e-commerce platform.",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_member_cannot_create_project(
        self, api_client, another_user, workspace, workspace_member, workflow
    ):
        api_client.force_authenticate(user=another_user)

        url = PROJECT_CREATE_URL.format(workspace.id, workflow.id)

        response = api_client.post(
            url,
            {
                "name": "E-commerce Platform",
                "description": "Develop the backend and API for the e-commerce platform.",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

    def test_owner_can_create_project(self, authenticated_client, workspace, workflow):
        url = PROJECT_CREATE_URL.format(workspace.id, workflow.id)

        response = authenticated_client.post(
            url,
            {
                "name": "E-commerce Platform",
                "description": "Develop the backend and API for the e-commerce platform.",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_admin_can_update_project(
        self,
        api_client,
        another_user,
        workspace,
        workspace_admin,
        project,
    ):
        api_client.force_authenticate(user=another_user)

        url = PROJECT_UPDATE_URL.format(
            workspace.id,
            project.id,
        )

        response = api_client.patch(
            url,
            {"name": "Shop"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        project.refresh_from_db()

        assert project.name == "Shop"

    def test_member_cannot_update_project(
        self,
        api_client,
        another_user,
        workspace,
        workspace_member,
        project,
    ):
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

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

        project.refresh_from_db()

        assert project.name == "E-commerce Platform"

    def test_manager_can_update_project(
        self,
        api_client,
        another_user,
        workspace,
        workspace_manager,
        project,
    ):
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

        assert response.status_code == status.HTTP_200_OK

        project.refresh_from_db()

        assert project.name == "Production"


WORKFLOW_STATUS_URL = "/api/v1/projects/{}/workflow_status/"
WORKFLOW_STATUS_DETAIL_URL = "/api/v1/projects/workflow_status/{}/"


@pytest.mark.django_db
class TestWorkflowStatusAPI:
    def test_list_workflows_status_requires_authentication(
        self,
        api_client,
        workflow,
    ):
        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_member_can_list_workflow_status(
        self,
        api_client,
        another_user,
        workflow,
        workspace_member,
    ):
        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 0

    def test_owner_can_list_workflows_status(
        self,
        authenticated_client,
        workspace,
        workflow,
    ):
        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_user_cannot_list_another_workspace_workflow_status(
        self,
        authenticated_client,
        workflow_status_another,
    ):
        url = WORKFLOW_STATUS_URL.format(workflow_status_another.workflow.id)
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

    def test_admin_can_create_workflow_status(
        self,
        api_client,
        another_user,
        workflow,
        status_obj,
        status_obj_another,
        workspace_admin,
    ):
        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = api_client.post(
            url,
            {"status_id": status_obj.id, "order": 1},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

        assert WorkflowStatus.objects.filter(
            workflow=workflow,
            status=status_obj,
            order=1,
        ).exists()

        re_creation = api_client.post(
            url,
            {
                "status_id": status_obj_another.id,
                "order": 1,
            },
            format="json",
        )

        assert re_creation.status_code == status.HTTP_400_BAD_REQUEST
        assert re_creation.data["detail"] == (
            "This order is already used in this workflow."
        )

    def test_manager_can_create_workflow_status(
        self, api_client, another_user, workflow, workspace_manager, status_obj
    ):
        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = api_client.post(
            url,
            {"status_id": status_obj.id, "order": 1},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert WorkflowStatus.objects.filter(
            workflow=workflow,
            status=status_obj,
            order=1,
        ).exists()

    def test_member_cannot_create_workflow_status(
        self, api_client, another_user, workflow, workspace_member, status_obj
    ):
        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = api_client.post(
            url,
            {"status_id": status_obj.id, "order": 1},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

    def test_owner_can_create_workflow_status(
        self,
        authenticated_client,
        status_obj,
        workflow,
    ):
        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = authenticated_client.post(
            url,
            {"status_id": status_obj.id, "order": 1},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_update_workflow_status(
        self,
        api_client,
        another_user,
        workspace_admin,
        workflow_status,
    ):
        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = api_client.patch(
            url,
            {"order": 2},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        workflow_status.refresh_from_db()

        assert workflow_status.order == 2

    def test_member_cannot_update_workflow_status(
        self,
        api_client,
        another_user,
        workspace_member,
        workflow_status,
    ):
        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = api_client.patch(
            url,
            {"order": 2},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

        workflow_status.refresh_from_db()

        assert workflow_status.order == 1

    def test_manager_can_update_workflow_status(
        self,
        api_client,
        another_user,
        workspace_manager,
        workflow_status,
    ):
        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = api_client.patch(
            url,
            {"order": 2},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        workflow_status.refresh_from_db()

        assert workflow_status.order == 2

    def test_delete_workflow_status(
        self,
        authenticated_client,
        workflow_status,
    ):
        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not WorkflowStatus.objects.filter(id=workflow_status.id).exists()

    def test_member_cannot_delete_workflow_status(
        self,
        api_client,
        another_user,
        workflow_status,
        workspace_member,
    ):
        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

        assert WorkflowStatus.objects.filter(id=workflow_status.id).exists()

    def test_delete_nonexistent_workflow_status(
        self,
        authenticated_client,
    ):
        url = WORKFLOW_STATUS_DETAIL_URL.format(99999)

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND


SPRINT_URL = "/api/v1/projects/workspaces/{}/projects/{}/sprints/"
SPRINT_DETAIL_URL = "/api/v1/projects/workspaces/{}/projects/{}/sprints/{}/"


@pytest.mark.django_db
class TestSprintAPI:
    def test_list_sprint_requires_authentication(
        self,
        api_client,
        workspace,
        project
    ):
        url = SPRINT_URL.format(workspace.id, project.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_member_can_list_sprint(
        self,
        api_client,
        another_user,
        workspace,
        project,
        workspace_member,
    ):
        api_client.force_authenticate(user=another_user)

        url = SPRINT_URL.format(workspace.id, project.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 0

    def test_owner_can_list_sprint(
        self,
        authenticated_client,
        workspace,
        project,
    ):
        url = SPRINT_URL.format(workspace.id, project.id)

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_user_cannot_list_another_workspace_sprint(
        self,
        authenticated_client,
        another_workspace,
        another_project,
    ):
        url = SPRINT_URL.format(another_workspace.id, another_project.id)

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

    def test_admin_can_create_sprint(
        self,
        api_client,
        another_user,
        workspace,
        project,
        workspace_admin,
    ):
        api_client.force_authenticate(user=another_user)

        url = SPRINT_URL.format(workspace.id, project.id)

        response = api_client.post(
            url,
            {
                "name": "sprint 1",
                "start_date": "2026-08-19T08:03:25.955Z",
                "end_date": "2026-09-19T08:03:25.955Z",
                "goal": "Complete authentication and project management features.",
            },
            format="json",
        )
        sprint = Sprint.objects.get(
            project=project,
            name="sprint 1",
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert sprint.start_date is not None
        assert sprint.end_date is not None
        assert sprint.goal == (
            "Complete authentication and project management features."
        )

        re_creation = api_client.post(
            url,
            {
                "name": "sprint 1",
                "start_date": "2026-09-19T08:03:25.955Z",
                "end_date": "2026-10-19T08:03:25.955Z",
                "goal": "Complete authentication features.",
            },
            format="json",
        )

        assert re_creation.status_code == status.HTTP_400_BAD_REQUEST
        assert re_creation.data["name"] == (
            "A sprint with this name already exists in this project."
        )

    def test_manager_can_create_sprint(
        self,
        api_client,
        another_user,
        workspace,
        project,
        workspace_manager,
    ):
        api_client.force_authenticate(user=another_user)

        url = SPRINT_URL.format(workspace.id, project.id)

        response = api_client.post(
            url,
            {
                "name": "sprint 1",
                "start_date": "2026-08-19T08:03:25.955Z",
                "end_date": "2026-09-19T08:03:25.955Z",
                "goal": "Complete authentication and project management features.",
            },
            format="json",
        )
        sprint = Sprint.objects.get(
            project=project,
            name="sprint 1",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert sprint.start_date is not None
        assert sprint.end_date is not None
        assert sprint.goal == (
            "Complete authentication and project management features."
        )


    def test_member_cannot_create_sprint(
        self,
        api_client,
        another_user,
        workspace,
        project,
    ):
        api_client.force_authenticate(user=another_user)

        url = SPRINT_URL.format(workspace.id, project.id)

        response = api_client.post(
            url,
            {
                "name": "sprint 1",
                "start_date": "2026-08-19T08:03:25.955Z",
                "end_date": "2026-09-19T08:03:25.955Z",
                "goal": "Complete authentication and project management features.",
            },
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
                "name": "sprint 1",
                "start_date": "2026-08-19T08:03:25.955Z",
                "end_date": "2026-09-19T08:03:25.955Z",
                "goal": "Complete authentication and project management features.",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_update_sprint(
        self,
        api_client,
        another_user,
        workspace_admin,
        workspace,
        project,
        sprint
    ):
        api_client.force_authenticate(user=another_user)

        url = SPRINT_DETAIL_URL.format(workspace.id, project.id, sprint.id)

        response = api_client.patch(
            url,
            {"name": "sprint2"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        sprint.refresh_from_db()

        assert sprint.name == "sprint2"

    def test_member_cannot_update_sprint(
        self,
        api_client,
        another_user,
        workspace_member,
        workspace,
        project,
        sprint
    ):
        api_client.force_authenticate(user=another_user)

        url = SPRINT_DETAIL_URL.format(workspace.id, project.id, sprint.id)

        response = api_client.patch(
            url,
            {"name": "sprint2"},
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

        sprint.refresh_from_db()

        assert sprint.name == "sprint 1"

    def test_manager_can_update_sprint(
        self,
        api_client,
        another_user,
        workspace_manager,
        workspace,
        project,
        sprint
    ):
        api_client.force_authenticate(user=another_user)

        url = SPRINT_DETAIL_URL.format(workspace.id, project.id, sprint.id)

        response = api_client.patch(
            url,
            {"name": "sprint2"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        sprint.refresh_from_db()
        
        assert sprint.name == "sprint2"

    def test_delete_sprint(
        self,
        authenticated_client,
        workspace,
        project,
        sprint
    ):
        url = SPRINT_DETAIL_URL.format(workspace.id, project.id, sprint.id)

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not Sprint.objects.filter(id=sprint.id).exists()

    def test_member_cannot_delete_sprint(
        self,
        api_client,
        another_user,
        workspace,
        project,
        sprint,
        workspace_member,
    ):
        api_client.force_authenticate(user=another_user)

        url = SPRINT_DETAIL_URL.format(workspace.id, project.id, sprint.id)

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

        assert Sprint.objects.filter(id=sprint.id).exists()

    def test_delete_nonexistent_sprint(
        self,
        authenticated_client,
        workspace,
        project,
    ):
        nonexistent_sprint_id = Sprint.objects.all().order_by("-id").first()

        sprint_id = (
            nonexistent_sprint_id.id + 1
            if nonexistent_sprint_id
            else 1
        )

        url = SPRINT_DETAIL_URL.format(
            workspace.id,
            project.id,
            sprint_id,
        )
        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
