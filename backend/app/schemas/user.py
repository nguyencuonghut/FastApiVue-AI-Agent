from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class UserCreateRequest(BaseModel):
    email: str
    password: str = Field(min_length=8)
    status: str = "active"
    role_names: list[str] = Field(default_factory=list)


class UserRoleUpdateRequest(BaseModel):
    role_names: list[str] = Field(default_factory=list)


class UserUpdateRequest(BaseModel):
    email: str
    status: str
    password: str | None = Field(default=None, min_length=8)
    role_names: list[str] = Field(default_factory=list)


class UserResponse(BaseModel):
    id: UUID
    email: str
    status: str
    roles: list[str]
    permissions: list[str]
    last_login_at: datetime | None


class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
