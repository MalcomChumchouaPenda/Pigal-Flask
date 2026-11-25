import inspect
import pytest
from unittest.mock import MagicMock
import pigal_flask.security.abstract as pkg


def test_is_abstract_class():
    with pytest.raises(TypeError):
        pkg.AccessProvider()


EXPECTED_ABSTRACT_METHODS = {
    "authenticate",
    "logout",
    "identity",
    "is_authenticated",
    "has_role",
    "has_permission",
}


def test_declare_expected_abstract_methods():
    methods = pkg.AccessProvider.__abstractmethods__
    assert methods == EXPECTED_ABSTRACT_METHODS


@pytest.mark.parametrize(
    ("method", "parameters"),
    [
        ("authenticate", ("self", "credentials")),
        ("logout", ("self",)),
        ("identity", ("self",)),
        ("has_role", ("self", "role")),
        ("has_permission", ("self", "permission")),
    ],
)
def test_method_signature(method, parameters):
    method = getattr(pkg.AccessProvider, method)
    signature = inspect.signature(method)
    assert tuple(signature.parameters) == parameters


class FakeProvider(pkg.AccessProvider):

    def authenticate(self, credentials):
        pass

    def logout(self):
        pass

    def identity(self):
        pass

    def is_authenticated(self):
        pass

    def has_role(self, role):
        pass

    def has_permission(self, permission):
        pass


def test_is_configured_with_store():
    store = MagicMock()
    provider = FakeProvider(store)
    assert provider.store is store
