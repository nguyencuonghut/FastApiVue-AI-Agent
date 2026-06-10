"""Authentication package scaffold."""

from app.auth.dependencies import get_current_user, oauth2_scheme
from app.auth.hashing import hash_password, needs_rehash, verify_password
from app.auth.jwt import AccessTokenPayload, AuthTokenError, decode_access_token, issue_access_token
from app.auth.service import (
    AccessTokenResult,
    AuthService,
    AuthSessionBundle,
    InactiveUserError,
    InvalidCredentialsError,
    RefreshTokenError,
    create_access_token_result,
)

__all__ = [
    "AccessTokenPayload",
    "AccessTokenResult",
    "AuthService",
    "AuthSessionBundle",
    "AuthTokenError",
    "InactiveUserError",
    "InvalidCredentialsError",
    "RefreshTokenError",
    "create_access_token_result",
    "decode_access_token",
    "get_current_user",
    "hash_password",
    "issue_access_token",
    "needs_rehash",
    "oauth2_scheme",
    "verify_password",
]
