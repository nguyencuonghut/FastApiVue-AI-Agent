from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models import audit_log, permission, refresh_token, role, user  # noqa: F401,E402
