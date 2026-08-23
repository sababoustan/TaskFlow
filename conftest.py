import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from apps.users.models import User
from apps.workspaces.models import Workspace


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="testuser@gmail.com",
        full_name="test",
        password="StrongPassword123",
        is_verified=True,
    )


@pytest.fixture
def unrelated_user(db):
    return User.objects.create_user(
        email="unrelated@gmail.com",
        password="StrongPassword123",
        is_verified=True,
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def another_user(db):
    User = get_user_model()

    return User.objects.create_user(
        email="another@gmail.com",
        full_name="Another User",
        password="StrongPassword123",
        is_verified=True,
    )


@pytest.fixture
def workspace(user):
    return Workspace.objects.create(
        owner=user,
        title="python",
    )


@pytest.fixture
def another_workspace(db, another_user):
    return Workspace.objects.create(
        owner=another_user,
        title="Another Workspace",
    )