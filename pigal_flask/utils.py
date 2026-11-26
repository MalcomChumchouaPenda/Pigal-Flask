
from abc import ABC, abstractmethod
from sqlalchemy.orm import declared_attr


def __find_key(cls):
    name_parts = cls.__module__.split(".")
    i = name_parts.index("models")
    return name_parts[i - 1]


@declared_attr
def bind_key(cls):
    return __find_key(cls)


@declared_attr
def tablename(cls):
    key = __find_key(cls)
    name = cls.__name__.lower()
    return f"{key}_{name}"


class Authenticator(ABC):

    @abstractmethod
    def is_authenticated(self):
        """Determine whether the current user is authenticated."""

    @abstractmethod
    def has_roles(self, *roles):
        """Determine whether the current user has at least one role."""

    @abstractmethod
    def on_unauthenticated(self):
        """Handle an unauthorized access attempt (authentification required)."""

    @abstractmethod
    def on_unauthorized(self):
        """Handle an unauthorized access attempt (insufficient permissions)."""

