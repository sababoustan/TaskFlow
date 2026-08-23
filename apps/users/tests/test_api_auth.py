import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

User = get_user_model()

REGISTER_URL = "/api/v1/auth/register/"
LOGIN_URL = "/api/v1/auth/login/"
LOGOUT_URL = "/api/v1/auth/logout/"
REFRESH_URL = "/api/v1/auth/token/refresh/"


@pytest.mark.django_db
class TestRegisterAPI:

    def test_register_user(self, api_client):
        response = api_client.post(
            REGISTER_URL,
            {
                "email": "newuser@gmail.com",
                "full_name": "newuser",
                "password": "StrongPassword123",
                "password1": "StrongPassword123",
            },
            format="json",
        )

        assert response.status_code == 201
        assert response.data["message"] == "User registered successfully."
        assert response.data["email"] == "newuser@gmail.com"


    def test_register_user_with_mismatched_passwords(
        self,
        api_client,
    ):
        response = api_client.post(
            REGISTER_URL,
            {
                "email": "newuser@gmail.com",
                "full_name": "newuser",
                "password": "StrongPassword123",
                "password1": "DifferentPassword123",
            },
            format="json",
        )

        assert response.status_code == 400
        assert "password1" in response.data


    def test_register_user_with_duplicate_email(
        self,
        api_client,
        user,
    ):
        response = api_client.post(
            REGISTER_URL,
            {
                "email": user.email,
                "full_name": "newuser",
                "password": "StrongPassword123",
                "password1": "StrongPassword123",
            },
            format="json",
        )

        assert response.status_code == 400
        assert "email" in response.data


@pytest.mark.django_db
class TestLoginAPI:

    def test_login_user(self, api_client, user):
        response = api_client.post(
            LOGIN_URL,
            {
                "email": user.email,
                "password": "StrongPassword123",
            },
            format="json",
        )

        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

        assert response.data["user"]["id"] == user.id
        assert response.data["user"]["email"] == user.email
        assert response.data["user"]["full_name"] == user.full_name
        assert response.data["user"]["is_verified"] is True


    def test_login_with_invalid_password(
        self,
        api_client,
        user,
    ):
        response = api_client.post(
            LOGIN_URL,
            {
                "email": user.email,
                "password": "WrongPassword123",
            },
            format="json",
        )

        assert response.status_code == 401
        assert response.data["detail"] == "Invalid email or password."


    def test_login_with_invalid_email(self, api_client):
        response = api_client.post(
            LOGIN_URL,
            {
                "email": "notexist@gmail.com",
                "password": "StrongPassword123",
            },
            format="json",
        )

        assert response.status_code == 401
        assert response.data["detail"] == "Invalid email or password."


    def test_unverified_user_cannot_login(
        self,
        api_client,
        user,
    ):
        user.is_verified = False
        user.save(update_fields=["is_verified"])

        response = api_client.post(
            LOGIN_URL,
            {
                "email": user.email,
                "password": "StrongPassword123",
            },
            format="json",
        )

        assert response.status_code == 401
        assert response.data["detail"] == "User account is not verified."


    def test_inactive_user_cannot_login(
        self,
        api_client,
        user,
    ):
        user.is_active = False
        user.save(update_fields=["is_active"])

        response = api_client.post(
            LOGIN_URL,
            {
                "email": user.email,
                "password": "StrongPassword123",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "Invalid email or password."


@pytest.mark.django_db
class TestLogoutAPI:

    def test_logout_user(
        self,
        api_client,
        user,
    ):
        refresh = RefreshToken.for_user(user)

        access = str(refresh.access_token)

        api_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access}"
        )

        response = api_client.post(
            LOGOUT_URL,
            {"refresh": str(refresh)},
            format="json",
        )

        assert response.status_code == 200
        assert response.data == {
            "message": "Logout successful."
        }

        assert BlacklistedToken.objects.filter(
            token__jti=refresh["jti"]
        ).exists()


    def test_logout_requires_authentication(
        self,
        api_client,
        user,
    ):
        refresh = RefreshToken.for_user(user)

        response = api_client.post(
            LOGOUT_URL,
            {"refresh": str(refresh)},
            format="json",
        )

        assert response.status_code == 401


    def test_logout_with_invalid_refresh_token(
        self,
        api_client,
        user,
    ):
        refresh = RefreshToken.for_user(user)

        access = str(refresh.access_token)

        api_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access}"
        )

        response = api_client.post(
            LOGOUT_URL,
            {"refresh": "invalid-refresh-token"},
            format="json",
        )

        assert response.status_code == 400


@pytest.mark.django_db
class TestRefreshTokenAPI:

    def test_refresh_token(self, api_client, user):
        refresh = RefreshToken.for_user(user)

        response = api_client.post(
            REFRESH_URL,
            {"refresh": str(refresh)},
            format="json",
        )

        assert response.status_code == 200
        assert "access" in response.data


PROFILE_URL = "/api/v1/auth/profile/"


@pytest.mark.django_db
def test_profile(client, user):
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    response = client.get(PROFILE_URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email
    assert response.data["full_name"] == user.full_name


@pytest.mark.django_db
def test_profile_update(client, user):
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    response = client.put(
        PROFILE_URL,
        {"full_name": "new-user"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["full_name"] == "new-user"

    user.refresh_from_db()

    assert user.full_name == "new-user"


ACCOUNT_URL = "/api/v1/auth/account/"


@pytest.mark.django_db
def test_delete_account(client, user):
    access = AccessToken.for_user(user)

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    response = client.delete(ACCOUNT_URL)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(id=user.id).exists()


CHANGE_PASSWORD_URL = "/api/v1/auth/change-password/"


@pytest.mark.django_db
def test_change_password(client, user):
    refresh = RefreshToken.for_user(user)

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )

    response = client.put(
        CHANGE_PASSWORD_URL,
        {
            "old_password": "StrongPassword123",
            "new_password": "StrongPassword1234",
            "confirm_password": "StrongPassword1234",
        },
        format="json",
    )

    user.refresh_from_db()

    refresh_response = client.post(
        "/api/v1/auth/token/refresh/",
        {"refresh": str(refresh)},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "message": "Password changed successfully."
    }

    assert user.check_password("StrongPassword1234")

    assert BlacklistedToken.objects.filter(
        token__jti=refresh["jti"]
    ).exists()

    assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED
