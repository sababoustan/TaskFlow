import pytest
from rest_framework.test import APIClient

from apps.users.models import User
from apps.workspaces.models import Workspace


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
def workspace(user):
    return Workspace.objects.create(
        owner=user,
        title="python",
    )
