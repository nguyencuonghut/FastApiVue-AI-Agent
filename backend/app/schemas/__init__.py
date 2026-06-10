"""Pydantic schemas package."""

from app.schemas.auth import AccessTokenResponse, CurrentUserResponse, LoginRequest
from app.schemas.permission import PermissionResponse
from app.schemas.role import (
    RoleCreateRequest,
    RoleListResponse,
    RoleResponse,
    RoleUpdateRequest,
)
from app.schemas.user import (
    UserCreateRequest,
    UserListResponse,
    UserResponse,
    UserRoleUpdateRequest,
    UserUpdateRequest,
)

__all__ = [
    "AccessTokenResponse",
    "CurrentUserResponse",
    "LoginRequest",
    "PermissionResponse",
    "RoleCreateRequest",
    "RoleListResponse",
    "RoleResponse",
    "RoleUpdateRequest",
    "UserCreateRequest",
    "UserListResponse",
    "UserResponse",
    "UserRoleUpdateRequest",
    "UserUpdateRequest",
]
