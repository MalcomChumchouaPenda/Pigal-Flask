from collections import defaultdict
from .abstract import AccessStore, AccessProvider


class MemoryAccessStore(AccessStore):

    def __init__(self):
        self._users = {}
        self._roles = {}

        # user_id -> set(role_name)
        self._user_roles = defaultdict(set)

        # role_name -> set(permission)
        self._role_permissions = defaultdict(set)

    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------

    def create_user(self, user_id, user_pwd, **kwargs):
        user = kwargs
        user.update(id=user_id, pwd=user_pwd)
        self._users[user_id] = user

    def find_user(self, user_id):
        user = self._users.get(user_id)
        if user:
            user_perms = []
            roles = self.find_user_roles(user_id)
            for role_id in roles:
                role_perms = self.find_role_permissions(role_id)
                user_perms.extend(list(role_perms))
            user = user.copy()
            user["roles"] = roles
            user["permissions"] = set(user_perms)
            return user

    def update_user(self, user_id, **kwargs):
        user = self._users[user_id]
        user.update(**kwargs)

    def delete_user(self, user_id):
        self._users.pop(user_id, None)
        self._user_roles.pop(user_id, None)

    # ------------------------------------------------------------------
    # Roles
    # ------------------------------------------------------------------

    def create_role(self, role):
        self._roles[role] = role
        return role

    def find_role(self, role_name):
        return self._roles.get(role_name)

    def update_role(self, role):
        self._roles[role] = role
        return role

    def delete_role(self, role_name):
        self._roles.pop(role_name, None)
        self._role_permissions.pop(role_name, None)
        for roles in self._user_roles.values():
            roles.discard(role_name)

    # ------------------------------------------------------------------
    # Permissions
    # ------------------------------------------------------------------

    def grant_permission(self, role, permission):
        self._role_permissions[role].add(permission)

    def revoke_permission(self, role, permission):
        self._role_permissions[role].discard(permission)

    # ------------------------------------------------------------------
    # RBAC
    # ------------------------------------------------------------------

    def assign_role(self, user, role):
        self._user_roles[user].add(role)

    def revoke_role(self, user, role):
        self._user_roles[user].discard(role)

    def find_user_roles(self, user):
        return frozenset(self._user_roles.get(user, ()))

    def find_role_permissions(self, role):
        return frozenset(self._role_permissions.get(role, ()))


class MemoryAccessProvider(AccessProvider):

    def __init__(self, store):
        super().__init__(store)
        self._identity = None

    def authenticate(self, credentials):
        user = self.store.find_user(credentials["user_id"])
        if user is None or user["user_pwd"] != credentials["user_pwd"]:
            return False
        user.pop("user_pwd")
        self._identity = user
        return True

    def logout(self):
        self._identity = None

    def identity(self):
        return self._identity

    def is_authenticated(self):
        return self._identity is not None

    def has_role(self, role):
        if not self._identity:
            return False
        return role in self._identity["roles"]

    def has_permission(self, permission):
        if not self._identity:
            return False
        return permission in self._identity["permissions"]


class MemoryUser:
    pass


class MemoryRole:
    pass


class MemoryPermission:
    pass
