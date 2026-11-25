import os
import sys
from unittest.mock import MagicMock

import pytest
import pigal_flask as pkg
from pigal_flask import extensions as ext
from pigal_flask import exceptions as exc


@pytest.fixture
def project_manager(monkeypatch):
    MockUi = MagicMock(return_value=MagicMock(spec=pkg.Ui))
    MockRestApi = MagicMock(return_value=MagicMock(spec=pkg.RestApi))
    monkeypatch.setattr(pkg, "Ui", MockUi)
    monkeypatch.setattr(pkg, "RestApi", MockRestApi)
    monkeypatch.setattr(ext, "Api", MagicMock())
    monkeypatch.setattr(ext, "Blueprint", MagicMock())
    project_manager = ext.ProjectManager()
    return project_manager


@pytest.fixture
def project1(tmp_path_factory, monkeypatch):
    """Empty project dir"""
    project_dir = tmp_path_factory.mktemp("fake")
    monkeypatch.syspath_prepend(str(project_dir))
    return project_dir


@pytest.fixture
def app1(project1):
    """App without config"""
    app = MagicMock()
    app.instance_path = str(project1 / "app/__init__.py")
    return app


def test_require_app_dir_in_project(project_manager, app1, project1):
    modules_dir = project1 / "modules"
    modules_dir.mkdir()

    with pytest.raises(exc.InvalidProjectStructure) as exc_info:
        project_manager.init_app(app1)
    err_msg = "'app' directory is required but not found"
    assert str(exc_info.value) == err_msg


def test_require_modules_dir_in_project(project_manager, app1, project1):
    app_dir = project1 / "app"
    app_dir.mkdir()

    with pytest.raises(exc.InvalidProjectStructure) as exc_info:
        project_manager.init_app(app1)
    err_msg = "'modules' directory is required but not found"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def project2(project1):
    """project with app and modules dirs"""
    (project1 / "app").mkdir()
    (project1 / "modules").mkdir()
    yield project1
    for name in list(sys.modules):
        if name.startswith("modules"):
            sys.modules.pop(name)


@pytest.mark.usefixtures("project2")
def test_require_project_name_in_config(app1, project_manager):
    app1.config = {"PIGAL_PROJECT_VERSION": "1.0"}

    with pytest.raises(exc.InvalidProjectConfig) as exc_info:
        project_manager.init_app(app1)
    err_msg = "Configuration parameter 'PIGAL_PROJECT_NAME' is missing"
    assert str(exc_info.value) == err_msg


@pytest.mark.usefixtures("project2")
def test_require_project_version_in_config(app1, project_manager):
    app1.config = {"PIGAL_PROJECT_NAME": "test"}

    with pytest.raises(exc.InvalidProjectConfig) as exc_info:
        project_manager.init_app(app1)
    err_msg = "Configuration parameter 'PIGAL_PROJECT_VERSION' is missing"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app2(app1):
    """app with minimal config"""
    app = app1
    app.config = {"PIGAL_PROJECT_NAME": "demo", "PIGAL_PROJECT_VERSION": "0.1"}
    return app


@pytest.mark.usefixtures("project2")
def test_create_main_rest_api(app2, project_manager):
    bp_name = ext.__name__
    project_manager.init_app(app2)

    main_rest_api = ext.Api.return_value
    api_bp = ext.Blueprint.return_value
    ext.Blueprint.assert_called_with("api", bp_name, url_prefix="/api")
    ext.Api.assert_called_with(api_bp, title="demo API", version="0.1")
    app2.register_blueprint.assert_any_call(api_bp)
    assert project_manager.api == main_rest_api


@pytest.fixture
def project3(project2):
    """project with private and public demo pages"""
    (project2 / "modules/demo").mkdir(parents=True)
    (project2 / "modules/_demo").mkdir(parents=True)
    return project2


UI_CODE = """
    \nfrom pigal_flask import Ui
    \nui = Ui(__name__)
    """


def test_register_module_ui_as_blueprint(app2, project3, project_manager):
    routes_file = project3 / "modules/demo/views.py"
    routes_file.write_text(UI_CODE, encoding="utf-8")
    project_manager.init_app(app2)

    ui = pkg.Ui.return_value
    app2.register_blueprint.assert_any_call(ui, url_prefix="/demo")


def test_register_home_ui_with_no_prefix(app2, project3, project_manager):
    (project3 / "modules/home").mkdir(parents=True)
    routes_file = project3 / "modules/home/views.py"
    routes_file.write_text(UI_CODE, encoding="utf-8")
    project_manager.init_app(app2)

    ui = pkg.Ui.return_value
    app2.register_blueprint.assert_any_call(ui, url_prefix="/")


def test_call_module_ui_for_scanning(app2, project3, project_manager):
    routes_file = project3 / "modules/demo/views.py"
    routes_file.write_text(UI_CODE, encoding="utf-8")
    project_manager.init_app(app2)

    ui = pkg.Ui.return_value
    ui.scan_pages.assert_any_call()


def test_ignore_private_module_ui(app2, project3, project_manager):
    routes_file = project3 / "modules/_demo/views.py"
    routes_file.write_text(UI_CODE, encoding="utf-8")
    project_manager.init_app(app2)

    with pytest.raises(AssertionError):
        ui = pkg.Ui.return_value
        app2.register_blueprint.assert_any_call(ui, url_prefix="/_demo")


def test_ignore_invalid_module_ui(app2, project3, project_manager):
    routes_file = project3 / "modules/demo/views.py"
    routes_file.write_text("ui = object()", encoding="utf-8")

    with pytest.raises(exc.InvalidUi) as exc_info:
        project_manager.init_app(app2)
    err_msg = "modules.demo.views.ui is not an instance of Ui"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def project4(project2):
    """project with private and public demo resources"""
    (project2 / "modules/demo/resources").mkdir(parents=True)
    (project2 / "modules/_demo/resources").mkdir(parents=True)
    return project2


API_CODE = """
    \nfrom pigal_flask import RestApi
    \nrest_api = RestApi(__file__)
    """


def test_register_module_rest_api_as_namespace(app2, project4, project_manager):
    routes_file = project4 / "modules/demo/resources.py"
    routes_file.write_text(API_CODE, encoding="utf-8")
    project_manager.init_app(app2)

    path = "/demo/v0"
    module_rest_api = pkg.RestApi.return_value
    main_rest_api = ext.Api.return_value
    main_rest_api.add_namespace.assert_any_call(module_rest_api, path=path)


def test_ignore_private_module_rest_api(app2, project4, project_manager):
    routes_file = project4 / "modules/_demo/resources.py"
    routes_file.write_text(API_CODE, encoding="utf-8")
    project_manager.init_app(app2)

    with pytest.raises(AssertionError):
        path = "/_demo/v0"
        main_rest_api = ext.Api.return_value
        module_rest_api = pkg.RestApi.return_value
        print("testing", main_rest_api, module_rest_api, path)
        main_rest_api.add_namespace.assert_any_call(module_rest_api, path=path)


def test_ignore_invalid_module_rest_api(app2, project4, project_manager):
    routes_file = project4 / "modules/demo/resources.py"
    routes_file.write_text("rest_api = object()", encoding="utf-8")

    with pytest.raises(exc.InvalidRestApi) as exc_info:
        project_manager.init_app(app2)
    err_msg = "modules.demo.resources.rest_api "
    err_msg += "is not an instance of RestApi"
    assert str(exc_info.value) == err_msg


