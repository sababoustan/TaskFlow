import pytest


@pytest.mark.django_db
def test_create_user(user):
    assert user.email == "testuser@gmail.com"
    assert user.full_name == "test"
    assert user.is_verified is True
    assert user.is_active is True
