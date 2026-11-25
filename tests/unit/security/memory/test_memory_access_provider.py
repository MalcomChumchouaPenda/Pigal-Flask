import sys
import pytest
from unittest.mock import MagicMock
from werkzeug.exceptions import Unauthorized
import pigal_flask.security.memory as pkg


def test_is_concrete_access_provider():
    assert issubclass(pkg.MemoryAccessProvider, pkg.AccessProvider)


@pytest.fixture
def store():
    return MagicMock()


@pytest.fixture
def provider(store):
    return pkg.MemoryAccessProvider(store)


def test_keeps_store(provider, store):
    assert provider.store is store


def test_identity_is_anonymous_by_default(provider):
    assert provider.identity() is None
    assert provider.is_authenticated() is False


def test_authenticate_valid_credentials(provider, store):
    store.find_user.return_value = {"user_id": "admin", "user_pwd": "15"}
    ok = provider.authenticate({"user_id": "admin", "user_pwd": "15"})
    assert ok is True
    assert provider.is_authenticated()


def test_authenticate_sets_identity(provider, store):
    store.find_user.return_value = {"user_id": "admin", "user_pwd": "15"}
    provider.authenticate({"user_id": "admin", "user_pwd": "15"})
    assert provider.identity() == {"user_id": "admin"}


@pytest.mark.parametrize(
    ("user", "pwd", "result"),
    [("john", "ab", {"user_id": "john", "user_pwd": "15"}), ("ana", "15", None)],
)
def test_authenticate_invalid_credentials(provider, store, user, pwd, result):
    store.find_user.return_value = result
    ok = provider.authenticate({"user_id": user, "user_pwd": pwd})
    assert ok is False
    assert provider.identity() is None


def test_logout(provider, store):
    store.find_user.return_value = {"user_id": "admin", "user_pwd": "15"}
    provider.authenticate({"user_id": "admin", "user_pwd": "15"})
    provider.logout()
    assert provider.identity() is None
    assert not provider.is_authenticated()


@pytest.fixture
def user1():
    return {"user_id": "admin", "user_pwd": "15", "roles": {"admin"}}


def test_has_existing_role(provider, store, user1):
    store.find_user.return_value = user1
    provider.authenticate({"user_id": "admin", "user_pwd": "15"})
    assert provider.has_role("admin")


def test_has_unknown_role(provider, store, user1):
    store.find_user.return_value = user1
    provider.authenticate({"user_id": "admin", "user_pwd": "15"})
    assert not provider.has_role("editor")


def test_anonymous_has_no_role(provider):
    assert not provider.has_role("admin")


@pytest.fixture
def user2():
    return {"user_id": "admin", "user_pwd": "15", "permissions": {"users.read"}}


def test_has_existing_permission(provider, store, user2):
    store.find_user.return_value = user2
    provider.authenticate({"user_id": "admin", "user_pwd": "15"})
    assert provider.has_permission("users.read")


def test_has_unknown_permission(provider, store, user2):
    store.find_user.return_value = user2
    provider.authenticate({"user_id": "admin", "user_pwd": "15"})
    assert not provider.has_permission("users.write")


def test_anonymous_has_no_permission(provider):
    assert not provider.has_permission("users.read")


def test_identity_returns_current_identity(provider, store, user2):
    store.find_user.return_value = user2
    provider.authenticate({"user_id": "admin", "user_pwd": "15"})
    identity = provider.identity()
    assert identity is provider.identity()
