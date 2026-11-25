import sys
import pytest
from unittest.mock import MagicMock
from werkzeug.exceptions import Unauthorized
from pigal_flask import exceptions as exc
from pigal_flask import extensions as ext


@pytest.fixture
def project_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / "fake"
    project_dir.mkdir(parents=True)
    monkeypatch.syspath_prepend(str(project_dir))
    return project_dir


class FakeStore:
    pass


class FakeProvider:
    def __init__(self, store=None):
        self.store = store


ACCESS_CODE1 = """
    \nfrom pigal_flask.security import AccessProvider, AccessStore
    \nclass SomeStore(AccessStore): pass
    \nclass SomeProvider(AccessProvider): pass
    """


@pytest.fixture
def access_file(project_dir, monkeypatch):
    sys.modules.pop("modules.auth.services.access", None)
    access_dir = project_dir / "modules/auth/services"
    access_dir.mkdir(parents=True)
    access_file = access_dir / "access.py"
    access_file.write_text(ACCESS_CODE1, encoding="utf-8")
    monkeypatch.setattr("pigal_flask.security.AccessStore", FakeStore)
    monkeypatch.setattr("pigal_flask.extensions.AccessStore", FakeStore)
    monkeypatch.setattr("pigal_flask.security.AccessProvider", FakeProvider)
    monkeypatch.setattr("pigal_flask.extensions.AccessProvider", FakeProvider)
    return access_file


@pytest.fixture
def app(project_dir):
    app = MagicMock()
    app.instance_path = str(project_dir / "app/__init__.py")
    app.extensions = {}
    return app


@pytest.fixture
def access1(app):
    app.config = {
        "PIGAL_ACCESS_STORE_CLASS": "SomeStore",
        "PIGAL_ACCESS_PROVIDER_CLASS": "SomeProvider",
    }
    return ext.AccessManager()


@pytest.mark.usefixtures("access_file")
def test_init_app_loads_store(access1, app):
    access1.init_app(app)
    assert isinstance(access1.store, FakeStore)


@pytest.mark.usefixtures("access_file")
def test_init_app_without_store_raises_error(access1, app):
    app.config.pop("PIGAL_ACCESS_STORE_CLASS", None)
    with pytest.raises(exc.InvalidAppConfig) as exc_info:
        access1.init_app(app)
    err_msg = "PIGAL_ACCESS_STORE_CLASS is not configured"
    assert str(exc_info.value) == err_msg


ACCESS_CODE2 = """
    \nfrom pigal_flask.security import AccessProvider, AccessStore
    \nclass SomeStore: pass
    \nclass SomeProvider(AccessProvider): pass
    """


@pytest.mark.usefixtures("access_file")
def test_init_app_rejects_invalid_store(access1, app, project_dir):
    access_file = project_dir / "modules/auth/services/access.py"
    access_file.write_text(ACCESS_CODE2, encoding="utf-8")

    with pytest.raises(TypeError) as exc_info:
        access1.init_app(app)
    err_msg = "<class 'modules.auth.services.access.SomeStore'> "
    err_msg += "is not valid AccessStore"
    assert str(exc_info.value) == err_msg


@pytest.mark.usefixtures("access_file")
def test_init_app_loads_provider_with_store(access1, app):
    access1.init_app(app)
    assert isinstance(access1.provider, FakeProvider)
    assert access1.provider.store is access1.store


@pytest.mark.usefixtures("access_file")
def test_init_app_without_provider_raises_error(access1, app):
    app.config.pop("PIGAL_ACCESS_PROVIDER_CLASS", None)
    with pytest.raises(exc.InvalidAppConfig) as exc_info:
        access1.init_app(app)
    err_msg = "PIGAL_ACCESS_PROVIDER_CLASS is not configured"
    assert str(exc_info.value) == err_msg


ACCESS_CODE3 = """
    \nfrom pigal_flask.security import AccessProvider, AccessStore
    \nclass SomeStore(AccessStore): pass
    \nclass SomeProvider: pass
    """


@pytest.mark.usefixtures("access_file")
def test_init_app_rejects_invalid_provider(access1, app, project_dir):
    access_file = project_dir / "modules/auth/services/access.py"
    access_file.write_text(ACCESS_CODE3, encoding="utf-8")

    with pytest.raises(TypeError) as exc_info:
        access1.init_app(app)
    err_msg = "<class 'modules.auth.services.access.SomeProvider'> "
    err_msg += "is not valid AccessProvider"
    assert str(exc_info.value) == err_msg


@pytest.mark.usefixtures("access_file")
def test_init_app_registers_extension(access1, app):
    access1.init_app(app)
    assert app.extensions["access"] is access1


@pytest.fixture
def provider():
    return MagicMock()


@pytest.fixture
def access2(provider):
    access = ext.AccessManager()
    access.provider = provider
    return access


def test_identity_delegates_to_provider(access2, provider):
    user = object()
    provider.identity.return_value = user
    assert access2.identity() is user


def test_is_authenticated_delegates(access2, provider):
    provider.is_authenticated.return_value = True
    assert access2.is_authenticated()


def test_has_role_delegates(access2, provider):
    provider.has_role.return_value = True
    assert access2.has_role("admin")
    provider.has_role.assert_called_once_with("admin")


def test_has_permission_delegates(access2, provider):
    provider.has_permission.return_value = True
    assert access2.has_permission("user.read")
    provider.has_permission.assert_called_once_with("user.read")


def test_require_login_allows_authenticated_user(access2, provider):
    provider.is_authenticated.return_value = True

    @access2.require_login()
    def view():
        return "Hello"

    assert view() == "Hello"


def test_require_login_rejects_anonymous(access2, provider):
    provider.is_authenticated.return_value = False

    @access2.require_login()
    def view():
        return "Hello"

    with pytest.raises(Unauthorized):
        view()


def test_require_role_rejects_missing_role(access2, provider):
    provider.is_authenticated.return_value = True
    provider.has_role.return_value = False

    @access2.require_role("admin")
    def view():
        pass

    with pytest.raises(Exception):
        view()


def test_require_permission_accepts_permission(access2, provider):
    provider.is_authenticated.return_value = True
    provider.has_permission.return_value = True

    @access2.require_permission("users.read")
    def view():
        return "Hi"

    assert view() == "Hi"
