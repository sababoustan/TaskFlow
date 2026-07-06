import pytest
from apps.users.models import User
from rest_framework.test import APIClient    


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
    
    
