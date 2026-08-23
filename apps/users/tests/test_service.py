import pytest
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.services import (
    blacklist_refresh_token,
    blacklist_user_tokens,
)


@pytest.mark.django_db
class TestBlacklistRefreshToken:

    def test_blacklist_refresh_token(self, user):
        refresh = RefreshToken.for_user(user)

        blacklist_refresh_token(str(refresh))

        assert BlacklistedToken.objects.filter(
            token__jti=refresh["jti"]
        ).exists()


@pytest.mark.django_db
class TestBlacklistUserTokens:

    def test_blacklist_all_user_tokens(self, user):
        refresh_1 = RefreshToken.for_user(user)
        refresh_2 = RefreshToken.for_user(user)

        blacklist_user_tokens(user)

        assert BlacklistedToken.objects.filter(
            token__jti=refresh_1["jti"]
        ).exists()

        assert BlacklistedToken.objects.filter(
            token__jti=refresh_2["jti"]
        ).exists()

    def test_blacklist_user_tokens_does_not_affect_other_users(
        self,
        user,
        another_user,
    ):
        user_refresh = RefreshToken.for_user(user)
        another_user_refresh = RefreshToken.for_user(another_user)

        blacklist_user_tokens(user)

        assert BlacklistedToken.objects.filter(
            token__jti=user_refresh["jti"]
        ).exists()

        assert not BlacklistedToken.objects.filter(
            token__jti=another_user_refresh["jti"]
        ).exists()