# tests/functional/test_access_rbac.py

# import pytest
# from collections import defaultdict
# from flask import Flask
# from pigal_flask.extensions import AccessManager
# from pigal_flask.security import AccessStore
# from pigal_flask.security import AccessProvider



# class MemoryAccessProvider(AccessProvider):

#     def __init__(self, store):
#         super().__init__(store)
#         self._identity = None

#     # ------------------------------------------------------------------
#     # Authentication
#     # ------------------------------------------------------------------

#     def authenticate(self, user):
#         if self.store.find_user(user) is None:
#             raise ValueError(f"Unknown user: {user}")
#         self._identity = user

#     def logout(self):
#         self._identity = None

#     def identity(self):
#         return self._identity

#     def is_authenticated(self):
#         return self._identity is not None

#     # ------------------------------------------------------------------
#     # Authorization
#     # ------------------------------------------------------------------

#     def has_role(self, role):
#         if not self.is_authenticated():
#             return False
#         return role in self.store.roles(self._identity)

#     def has_permission(self, permission):
#         if not self.is_authenticated():
#             return False
#         for role in self.store.roles(self._identity):
#             if permission in self.store.permissions(role):
#                 return True
#         return False
    
# # ----------------------------------------------------------------------
# # Fixtures
# # ----------------------------------------------------------------------

# @pytest.fixture
# def store():
#     store = MemoryAccessStore()

#     # Roles
#     store.create_role("admin")
#     store.create_role("editor")
#     store.create_role("visitor")

#     # Permissions
#     store.grant_permission("admin", "users.read")
#     store.grant_permission("admin", "users.write")
#     store.grant_permission("admin", "users.delete")
#     store.grant_permission("editor", "users.read")
#     store.grant_permission("editor", "users.write")
#     store.grant_permission("visitor", "users.read")

#     # Users
#     store.create_user("alice")
#     store.create_user("bob")
#     store.create_user("charlie")

#     # Role assignments
#     store.assign_role("alice", "admin")
#     store.assign_role("bob", "editor")
#     store.assign_role("charlie", "visitor")
#     return store


# @pytest.fixture
# def provider(store):
#     return MemoryAccessProvider(store)


# @pytest.fixture
# def app(provider):
#     app = Flask(__name__)
#     access = AccessManager()
#     access.provider = provider
#     app.extensions["access"] = access

#     @app.get("/profile")
#     @access.require_login
#     def profile():
#         return "profile"

#     @app.get("/admin")
#     @access.require_role("admin")
#     def admin():
#         return "admin"

#     @app.get("/users")
#     @access.require_permission("users.read")
#     def users():
#         return "users"

#     @app.delete("/users")
#     @access.require_permission("users.delete")
#     def delete_users():
#         return "deleted"

#     return app


# @pytest.fixture
# def client(app):
#     return app.test_client()


# # ----------------------------------------------------------------------
# # require_login
# # ----------------------------------------------------------------------

# def test_require_login_accepts_authenticated(provider, client):

#     provider.authenticate("alice")

#     response = client.get("/profile")

#     assert response.status_code == 200


# def test_require_login_rejects_anonymous(client):

#     response = client.get("/profile")

#     assert response.status_code == 401


# # ----------------------------------------------------------------------
# # require_role
# # ----------------------------------------------------------------------

# def test_require_role_accepts(provider, client):

#     provider.authenticate("alice")

#     response = client.get("/admin")

#     assert response.status_code == 200


# def test_require_role_rejects(provider, client):

#     provider.authenticate("bob")

#     response = client.get("/admin")

#     assert response.status_code == 403


# # ----------------------------------------------------------------------
# # require_permission
# # ----------------------------------------------------------------------

# def test_require_permission_accepts(provider, client):

#     provider.authenticate("bob")

#     response = client.get("/users")

#     assert response.status_code == 200


# def test_require_permission_rejects(provider, client):

#     provider.authenticate("charlie")

#     response = client.delete("/users")

#     assert response.status_code == 403


# # ----------------------------------------------------------------------
# # Dynamic RBAC
# # ----------------------------------------------------------------------

# def test_assign_role_updates_permissions(store, provider, client):

#     provider.authenticate("bob")

#     response = client.delete("/users")
#     assert response.status_code == 403

#     store.assign_role("bob", "admin")

#     response = client.delete("/users")
#     assert response.status_code == 200


# def test_revoke_role_updates_permissions(store, provider, client):

#     provider.authenticate("alice")

#     response = client.delete("/users")
#     assert response.status_code == 200

#     store.revoke_role("alice", "admin")

#     response = client.delete("/users")
#     assert response.status_code == 403


# # ----------------------------------------------------------------------
# # Logout
# # ----------------------------------------------------------------------

# def test_logout(provider, client):
#     provider.authenticate("alice")

#     response = client.get("/profile")
#     assert response.status_code == 200

#     provider.logout()

#     response = client.get("/profile")
#     assert response.status_code == 401

