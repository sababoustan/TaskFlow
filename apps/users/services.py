from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework_simplejwt.tokens import RefreshToken


def blacklist_refresh_token(refresh_token):
    """Blacklist a single refresh token."""
    token = RefreshToken(refresh_token)
    token.blacklist()


def blacklist_user_tokens(user):
    """Blacklist all outstanding refresh tokens for a user."""
    for token in OutstandingToken.objects.filter(user=user):
        BlacklistedToken.objects.get_or_create(token=token)