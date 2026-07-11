import pytest
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import BlacklistedToken


User = get_user_model()


@pytest.mark.django_db
def test_register(client):
    response = client.post(
        "/api/v1/auth/register/",
        {
            "email": "newuser@gmail.com",
            "full_name": "newuser",
            "password": "StrongPassword123",
            "password1": "StrongPassword123"
         },
        format="json"
    )
    assert response.status_code == 201
    assert response.data["email"] == "newuser@gmail.com"


@pytest.mark.django_db
def test_login(user, client):
    response = client.post(
        "/api/v1/auth/login/",
        {
            "email": user.email,
            "password": "StrongPassword123",
        },
        format="json"
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_logout(client, user):
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
        )
    logout_response = client.post(
        "/api/v1/auth/logout/",
        {
            "refresh": str(refresh)
        },
        format="json"
    )
    refresh_response = client.post(
        "/api/v1/auth/token/refresh/",
        {
            "refresh": str(refresh)
        },
        format="json"
    )
    assert logout_response.status_code == 200
    assert logout_response.data == {"message": "Logout successful."}
    assert BlacklistedToken.objects.filter(
            token__jti=refresh["jti"]
        ).exists()
    assert refresh_response.status_code == 401


@pytest.mark.django_db
def test_profile(client, user):
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
    )
    response = client.get("/api/v1/auth/profile/")

    assert response.status_code == 200
    assert response.data["email"] == user.email
    assert response.data["full_name"] == user.full_name


@pytest.mark.django_db
def test_profile_update(client, user):
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access}"
    )
    response = client.put(
        "/api/v1/auth/profile/",
        {
            "full_name": "new-user"
        },
        format="json"
    )
    assert response.status_code == 200
    assert response.data["full_name"] == "new-user"


@pytest.mark.django_db
def test_delete_account(client, user):
    access = AccessToken.for_user(user)
    client.credentials(
    HTTP_AUTHORIZATION=f"Bearer {access}"
    )
    response = client.delete("/api/v1/auth/account/")

    assert response.status_code == 204
    assert not User.objects.filter(id=user.id).exists()


@pytest.mark.django_db
def test_change_password(client, user):
    refresh = RefreshToken.for_user(user)
    client.credentials(
    HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
    )
    response = client.put(
        "/api/v1/auth/change-password/",
        {
            "old_password": "StrongPassword123",
            "new_password": "StrongPassword1234",
            "confirm_password": "StrongPassword1234",
         },
        format="json"
    )

    user.refresh_from_db()

    refresh_response = client.post(
        "/api/v1/auth/token/refresh/",
        {
            "refresh": str(refresh)
        },
        format="json"
    )

    assert response.status_code == 200
    assert response.data == {
        "message": "Password changed successfully."
    }

    assert user.check_password("StrongPassword1234")

    assert BlacklistedToken.objects.filter(
        token__jti=refresh["jti"]
    ).exists()

    assert refresh_response.status_code == 401