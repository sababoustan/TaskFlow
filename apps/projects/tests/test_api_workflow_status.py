import pytest
from rest_framework import status

from apps.projects.models import WorkflowStatus


WORKFLOW_STATUS_URL = "/api/v1/projects/{}/workflow_status/"
WORKFLOW_STATUS_DETAIL_URL = "/api/v1/projects/workflow_status/{}/"


@pytest.mark.django_db
class TestWorkflowStatusAPI:

    def test_list_workflow_status_requires_authentication(
        self,
        api_client,
        workflow,
    ):
        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        "role",
        [
            "admin",
            "manager",
            "member",
            "viewer",
        ],
    )
    def test_workspace_roles_can_list_workflow_status(
        self,
        api_client,
        another_user,
        workflow,
        membership_factory,
        workflow_status,
        role,
    ):
        membership_factory(role)

        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 1

    def test_owner_can_list_workflow_status(
        self,
        authenticated_client,
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
        url = WORKFLOW_STATUS_URL.format(
            workflow_status_another.workflow.id
        )

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert response.data["detail"] == (
            "You do not have permission to perform this action."
        )

    def test_list_workflow_status_for_empty_workflow(
        self,
        authenticated_client,
        workflow,
    ):
        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"] == []

    @pytest.mark.parametrize(
        "role",
        [
            "admin",
            "manager",
        ],
    )
    def test_admin_and_manager_can_create_workflow_status(
        self,
        api_client,
        another_user,
        workflow,
        status_obj,
        membership_factory,
        role,
    ):
        membership_factory(role)

        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = api_client.post(
            url,
            {
                "status_id": status_obj.id,
                "order": 1,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        assert WorkflowStatus.objects.filter(
            workflow=workflow,
            status=status_obj,
            order=1,
        ).exists()

    def test_owner_can_create_workflow_status(
        self,
        authenticated_client,
        workflow,
        status_obj,
    ):
        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = authenticated_client.post(
            url,
            {
                "status_id": status_obj.id,
                "order": 1,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.parametrize(
        "role",
        [
            "member",
            "viewer",
        ],
    )
    def test_member_and_viewer_cannot_create_workflow_status(
        self,
        api_client,
        another_user,
        workflow,
        status_obj,
        membership_factory,
        role,
    ):
        membership_factory(role)

        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = api_client.post(
            url,
            {
                "status_id": status_obj.id,
                "order": 1,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_user_cannot_create_workflow_status(
        self,
        api_client,
        workflow,
        status_obj,
    ):
        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = api_client.post(
            url,
            {
                "status_id": status_obj.id,
                "order": 1,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_create_workflow_status_with_duplicate_order(
        self,
        authenticated_client,
        workflow,
        status_obj_another,
        workflow_status,
    ):
        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = authenticated_client.post(
            url,
            {
                "status_id": status_obj_another.id,
                "order": workflow_status.order,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert response.data["detail"] == (
            "This order is already used in this workflow."
        )

    def test_cannot_create_workflow_status_with_nonexistent_status(
        self,
        authenticated_client,
        workflow,
    ):
        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = authenticated_client.post(
            url,
            {
                "status_id": 99999,
                "order": 1,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cannot_create_workflow_status_without_status_id(
        self,
        authenticated_client,
        workflow,
    ):
        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = authenticated_client.post(
            url,
            {
                "order": 1,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "status_id" in response.data

    def test_cannot_create_workflow_status_without_order(
        self,
        authenticated_client,
        workflow,
        status_obj,
    ):
        url = WORKFLOW_STATUS_URL.format(workflow.id)

        response = authenticated_client.post(
            url,
            {
                "status_id": status_obj.id,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "order" in response.data

    def test_cannot_create_workflow_status_for_nonexistent_workflow(
        self,
        authenticated_client,
        status_obj,
    ):
        url = WORKFLOW_STATUS_URL.format(99999)

        response = authenticated_client.post(
            url,
            {
                "status_id": status_obj.id,
                "order": 1,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_admin_can_update_workflow_status(
        self,
        authenticated_client,
        workflow_status,
    ):
        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = authenticated_client.patch(
            url,
            {"order": 2},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        workflow_status.refresh_from_db()

        assert workflow_status.order == 2

    def test_manager_can_update_workflow_status(
        self,
        api_client,
        another_user,
        workflow_status,
        membership_factory,
    ):
        membership_factory("manager")

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

    @pytest.mark.parametrize(
        "role",
        [
            "member",
            "viewer",
        ],
    )
    def test_member_and_viewer_cannot_update_workflow_status(
        self,
        api_client,
        another_user,
        workflow_status,
        membership_factory,
        role,
    ):
        membership_factory(role)

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

        workflow_status.refresh_from_db()

        assert workflow_status.order == 1

    def test_unauthenticated_user_cannot_update_workflow_status(
        self,
        api_client,
        workflow_status,
    ):
        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = api_client.patch(
            url,
            {"order": 2},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cannot_update_workflow_status_to_same_order(
        self,
        authenticated_client,
        workflow_status,
    ):
        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = authenticated_client.patch(
            url,
            {"order": workflow_status.order},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        assert response.data["detail"] == (
            "This workflow status already has this order."
        )

    def test_cannot_update_workflow_status_to_duplicate_order(
        self,
        authenticated_client,
        workflow_status,
        workflow,
        status_obj_another,
    ):
        another_workflow_status = WorkflowStatus.objects.create(
            workflow=workflow,
            status=status_obj_another,
            order=2,
        )

        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = authenticated_client.patch(
            url,
            {"order": another_workflow_status.order},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        workflow_status.refresh_from_db()

        assert workflow_status.order == 1

    def test_update_nonexistent_workflow_status(
        self,
        authenticated_client,
    ):
        url = WORKFLOW_STATUS_DETAIL_URL.format(99999)

        response = authenticated_client.patch(
            url,
            {"order": 2},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_owner_can_delete_workflow_status(
        self,
        authenticated_client,
        workflow_status,
    ):
        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not WorkflowStatus.objects.filter(
            id=workflow_status.id
        ).exists()

    def test_admin_can_delete_workflow_status(
        self,
        api_client,
        another_user,
        workflow_status,
        membership_factory,
    ):
        membership_factory("admin")

        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not WorkflowStatus.objects.filter(
            id=workflow_status.id
        ).exists()

    @pytest.mark.parametrize(
        "role",
        [
            "manager",
            "member",
            "viewer",
        ],
    )
    def test_non_admin_cannot_delete_workflow_status(
        self,
        api_client,
        another_user,
        workflow_status,
        membership_factory,
        role,
    ):
        membership_factory(role)

        api_client.force_authenticate(user=another_user)

        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

        assert WorkflowStatus.objects.filter(
            id=workflow_status.id
        ).exists()

    def test_unauthenticated_user_cannot_delete_workflow_status(
        self,
        api_client,
        workflow_status,
    ):
        url = WORKFLOW_STATUS_DETAIL_URL.format(
            workflow_status.id,
        )

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_nonexistent_workflow_status(
        self,
        authenticated_client,
    ):
        url = WORKFLOW_STATUS_DETAIL_URL.format(99999)

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND