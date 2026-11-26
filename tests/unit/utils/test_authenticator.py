import inspect
import pytest
from unittest.mock import MagicMock
import pigal_flask.utils as pkg


def test_is_abstract_class():
    with pytest.raises(TypeError):
        pkg.Authenticator()


def test_declares_is_authenticated_method():
    method = getattr(pkg.Authenticator, "is_authenticated")
    assert method.__name__ in pkg.Authenticator.__abstractmethods__
    assert "self" in inspect.signature(method).parameters


def test_declares_has_roles_method():
    method = getattr(pkg.Authenticator, "has_roles")
    assert method.__name__ in pkg.Authenticator.__abstractmethods__
    assert "self" in inspect.signature(method).parameters
    assert "roles" in inspect.signature(method).parameters


def test_declares_on_unauthenticated_method():
    method = getattr(pkg.Authenticator, "on_unauthenticated")
    assert method.__name__ in pkg.Authenticator.__abstractmethods__
    assert "self" in inspect.signature(method).parameters


def test_declares_on_unauthorized_method():
    method = getattr(pkg.Authenticator, "on_unauthorized")
    assert method.__name__ in pkg.Authenticator.__abstractmethods__
    assert "self" in inspect.signature(method).parameters
