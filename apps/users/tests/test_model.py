import pytest

from apps.users.models import User


@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self):
        user = User.objects.create_user(
            email="testuser@gmail.com",
            password="StrongPassword123",
            full_name="test",
        )

        assert user.email == "testuser@gmail.com"
        assert user.full_name == "test"
        assert user.is_active is True
        assert user.is_verified is False

    def test_user_password_is_hashed(self):
        user = User.objects.create_user(
            email="testuser@gmail.com",
            password="StrongPassword123",
        )

        assert user.password != "StrongPassword123"
        assert user.check_password("StrongPassword123")

    def test_user_email_is_normalized(self):
        user = User.objects.create_user(
            email="TestUser@GMAIL.COM",
            password="StrongPassword123",
        )

        assert user.email == "testuser@gmail.com"

    def test_create_user_requires_email(self):
        with pytest.raises(
            ValueError,
            match="The email must be set.",
        ):
            User.objects.create_user(
                email="",
                password="StrongPassword123",
            )

    def test_create_user_requires_password(self):
        with pytest.raises(
            ValueError,
            match="Password must be set.",
        ):
            User.objects.create_user(
                email="testuser@gmail.com",
                password="",
            )

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@gmail.com",
            password="StrongPassword123",
        )

        assert user.is_superuser is True
        assert user.is_staff is True
        assert user.is_active is True

    def test_create_superuser_requires_is_staff(self):
        with pytest.raises(
            ValueError,
            match="Superuser must have is_staff=True",
        ):
            User.objects.create_superuser(
                email="admin@gmail.com",
                password="StrongPassword123",
                is_staff=False,
            )

    def test_create_superuser_requires_is_superuser(self):
        with pytest.raises(
            ValueError,
            match="Superuser must have is_superuser=True",
        ):
            User.objects.create_superuser(
                email="admin@gmail.com",
                password="StrongPassword123",
                is_superuser=False,
            )

    def test_user_str_returns_email(self):
        user = User.objects.create_user(
            email="testuser@gmail.com",
            password="StrongPassword123",
        )

        assert str(user) == "testuser@gmail.com"