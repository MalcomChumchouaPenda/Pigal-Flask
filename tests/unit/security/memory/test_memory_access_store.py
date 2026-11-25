import sys
import pytest
from unittest.mock import MagicMock
from werkzeug.exceptions import Unauthorized
import pigal_flask.security.memory as pkg


def test_is_concrete_access_store():
    assert issubclass(pkg.MemoryAccessStore, pkg.AccessStore)


@pytest.fixture
def store():
    return pkg.MemoryAccessStore()


def test_create_user(store):
    store.create_user("alice", "1234")
    assert store.find_user("alice") == {
        "id": "alice",
        "pwd": "1234",
        "roles": frozenset(),
        "permissions": frozenset(),
    }


def test_create_user_with_params(store):
    store.create_user("alice", "1234", name="alice")
    assert store.find_user("alice") == {
        "id": "alice",
        "pwd": "1234",
        "name": "alice",
        "roles": frozenset(),
        "permissions": frozenset(),
    }


def test_find_unknown_user_returns_none(store):
    assert store.find_user("alice") is None


def test_update_user(store):
    store.create_user("alice", "1234")
    store.update_user("alice", name="Alice Penda")
    assert store.find_user("alice") == {
        "id": "alice",
        "pwd": "1234",
        "name": "Alice Penda",
        "roles": frozenset(),
        "permissions": frozenset(),
    }


def test_delete_user(store):
    store.create_user("alice", "1234")
    store.delete_user("alice")
    assert store.find_user("alice") is None


def test_create_role(store):
    store.create_role("admin")
    assert store.find_role("admin") == "admin"


def test_find_unknown_role_returns_none(store):
    assert store.find_role("admin") is None


def test_delete_role(store):
    store.create_role("admin")
    store.delete_role("admin")
    assert store.find_role("admin") is None


def test_grant_permission(store):
    store.create_role("admin")
    store.grant_permission("admin", "users.read")
    assert "users.read" in store.find_role_permissions("admin")


def test_revoke_permission(store):
    store.create_role("admin")
    store.grant_permission("admin", "users.read")
    store.revoke_permission("admin", "users.read")
    assert "users.read" not in store.find_role_permissions("admin")


def test_assign_role(store):
    store.create_user("alice", "10")
    store.create_role("admin")
    store.assign_role("alice", "admin")
    assert store.find_user_roles("alice") == {"admin"}
    assert store.find_user("alice") == {
        "id": "alice",
        "pwd": "10",
        "roles": {"admin"},
        "permissions": frozenset(),
    }


def test_revoke_role(store):
    store.create_user("alice", "10")
    store.create_role("admin")
    store.assign_role("alice", "admin")
    store.revoke_role("alice", "admin")
    assert store.find_user_roles("alice") == frozenset()
    assert store.find_user("alice") == {
        "id": "alice",
        "pwd": "10",
        "roles": frozenset(),
        "permissions": frozenset(),
    }


def test_user_can_have_multiple_roles(store):
    store.create_user("alice", "10")
    store.create_role("admin")
    store.create_role("editor")
    store.assign_role("alice", "admin")
    store.assign_role("alice", "editor")
    assert store.find_user_roles("alice") == {"admin", "editor"}
    assert store.find_user("alice") == {
        "id": "alice",
        "pwd": "10",
        "roles": {"admin", "editor"},
        "permissions": frozenset(),
    }


def test_role_can_have_multiple_permissions(store):
    store.create_role("admin")
    store.grant_permission("admin", "users.read")
    store.grant_permission("admin", "users.write")
    assert store.find_role_permissions("admin") == {
        "users.read",
        "users.write",
    }


def test_assign_role_is_idempotent(store):
    store.create_user("alice", "12")
    store.create_role("admin")
    store.assign_role("alice", "admin")
    store.assign_role("alice", "admin")
    assert len(store.find_user_roles("alice")) == 1


def test_grant_permission_is_idempotent(store):
    store.create_role("admin")
    store.grant_permission("admin", "users.read")
    store.grant_permission("admin", "users.read")
    assert len(store.find_role_permissions("admin")) == 1


def test_delete_role_removes_permissions(store):
    store.create_role("admin")
    store.grant_permission("admin", "users.read")
    store.delete_role("admin")
    assert store.find_role_permissions("admin") == frozenset()


def test_delete_role_removes_assignments(store):
    store.create_user("alice", "12")
    store.create_role("admin")
    store.assign_role("alice", "admin")
    store.delete_role("admin")
    assert "admin" not in store.find_user_roles("alice")


def test_delete_user_removes_role_assignments(store):
    store.create_user("alice", "12")
    store.create_role("admin")
    store.assign_role("alice", "admin")
    store.delete_user("alice")
    assert store.find_user_roles("alice") == frozenset()
