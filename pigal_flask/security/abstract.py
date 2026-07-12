
from abc import ABC, abstractmethod


class AccessProvider(ABC):

    def __init__(self, store):
        super().__init__()
        self.store = store


    @abstractmethod
    def authenticate(self, credentials):
        """
        Authentifie un utilisateur et initialise
        l'identité courante.
        """

    @abstractmethod
    def logout(self):
        """
        Supprime l'identité courante.
        """

    @abstractmethod
    def identity(self):
        """
        Retourne l'identité courante ou None.
        """

    @abstractmethod
    def is_authenticated(self):
        """
        Indique si une identité valide existe.
        """

    @abstractmethod
    def has_role(self, role):
        """
        Vérifie un rôle.
        """

    @abstractmethod
    def has_permission(self, permission):
        """
        Vérifie une permission.
        """


class AccessStore(ABC):
    """
    Abstract storage backend for RBAC.

    The AccessStore is responsible for persisting users,
    roles and user-role assignments.
    """

    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------

    @abstractmethod
    def create_user(self, user_id, user_pwd, **kwargs):
        """Create a user."""

    @abstractmethod
    def find_user(self, user_id):
        """Return a user or None."""

    @abstractmethod
    def update_user(self, user_id, **kwargs):
        """Update a user."""

    @abstractmethod
    def delete_user(self, user_id):
        """Delete a user."""

    # ------------------------------------------------------------------
    # Roles
    # ------------------------------------------------------------------

    @abstractmethod
    def create_role(self, role_id, **kwargs):
        """Create a role."""

    @abstractmethod
    def find_role(self, role_id):
        """Return a role or None."""

    @abstractmethod
    def update_role(self, role_id, **kwargs):
        """Update a role."""

    @abstractmethod
    def delete_role(self, role_id):
        """Delete a role."""

    # ------------------------------------------------------------------
    # RBAC
    # ------------------------------------------------------------------

    @abstractmethod
    def assign_role(self, user_id, role_id):
        """Assign a role to a user."""

    @abstractmethod
    def revoke_role(self, user_id, role_id):
        """Revoke a role from a user."""

    @abstractmethod
    def find_user_roles(self, user_id):
        """Return the user's roles."""

    @abstractmethod
    def grant_permission(self, role_id, permission):
        """Grant a permission to a role."""

    @abstractmethod
    def revoke_permission(self, role_id, permission):
        """Revoke a permission from a role."""

    @abstractmethod
    def find_role_permissions(self, role_id):
        """Return the permissions attached to a role."""


class AccessUser:
    pass


class AccessRole:
    pass


class AccessPermission:
    pass

