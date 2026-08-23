import pytest
from rest_framework import status
from apps.projects.models import Status

STATUS_URL = "/api/v1/projects/statuses/"


@pytest.mark.django_db
class TestStatusAPI:
    def test_list_status_requires_authentication(
        self,
        api_client,
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

    def test_unauthenticated_user_cannot_create_status(
        self,
        api_client,
    ):
        response = api_client.post(
            STATUS_URL,
            {"name": "In Progress"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

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

    def test_admin_cannot_create_status_without_name(
        self,
        admin_client,
    ):
        response = admin_client.post(
            STATUS_URL,
            {},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_admin_cannot_create_duplicate_status(
        self,
        admin_client,
        status_obj,
    ):
        response = admin_client.post(
            STATUS_URL,
            {"name": status_obj.name},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_admin_cannot_create_status_with_name_longer_than_100_characters(
        self,
        admin_client,
    ):
        response = admin_client.post(
            STATUS_URL,
            {"name": "A" * 101},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

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

    def test_unauthenticated_user_cannot_update_status(
        self,
        api_client,
        status_obj,
    ):
        url = f"{STATUS_URL}{status_obj.id}/"

        response = api_client.patch(
            url,
            {"name": "Done"},
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

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

    def test_admin_cannot_update_status_to_duplicate_name(
        self,
        admin_client,
        status_obj,
        status_obj_another,
    ):
        url = f"{STATUS_URL}{status_obj.id}/"

        response = admin_client.patch(
            url,
            {"name": status_obj_another.name},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "name" in response.data

    def test_admin_can_delete_status(
        self,
        admin_client,
        status_obj,
    ):
        url = f"{STATUS_URL}{status_obj.id}/"

        response = admin_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Status.objects.filter(id=status_obj.id).exists()

    def test_unauthenticated_user_cannot_delete_status(
        self,
        api_client,
        status_obj,
    ):
        url = f"{STATUS_URL}{status_obj.id}/"

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_cannot_delete_status(
        self,
        authenticated_client,
        status_obj,
    ):
        url = f"{STATUS_URL}{status_obj.id}/"

        response = authenticated_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Status.objects.filter(id=status_obj.id).exists()

    def test_admin_cannot_update_nonexistent_status(
        self,
        admin_client,
    ):
        url = f"{STATUS_URL}99999/"

        response = admin_client.patch(
            url,
            {"name": "Done"},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_admin_cannot_delete_nonexistent_status(
        self,
        admin_client,
    ):
        url = f"{STATUS_URL}99999/"

        response = admin_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND