
import sys
from unittest.mock import MagicMock

import pytest
import pigal_flask as pkg
from pigal_flask import extensions as ext
from pigal_flask import exceptions as exc


@pytest.fixture
def route_manager(monkeypatch):
    MockModuleUi = MagicMock(return_value=MagicMock(spec=pkg.ModuleUi))
    MockApi = MagicMock(return_value=MagicMock(spec=pkg.ModuleApi))
    monkeypatch.setattr(pkg, 'ModuleUi', MockModuleUi)
    monkeypatch.setattr(pkg, 'ModuleApi', MockApi)
    monkeypatch.setattr(ext, 'Api', MagicMock())
    monkeypatch.setattr(ext, 'Blueprint', MagicMock())
    route_manager = ext.RouteManager()
    return route_manager

    
@pytest.fixture
def project1(tmp_path_factory, monkeypatch):
    """Empty project dir"""
    project_dir = tmp_path_factory.mktemp('fake')
    monkeypatch.syspath_prepend(str(project_dir))
    return project_dir


@pytest.fixture
def app1(project1):
    """App without config"""
    app = MagicMock()
    app.instance_path = str(project1 / 'app/__init__.py')
    return app


def test_requires_app_dir_in_project(route_manager, app1, project1):
    modules_dir = project1 / 'modules'
    modules_dir.mkdir()

    with pytest.raises(exc.InvalidProjectStructure) as exc_info:
        route_manager.init_app(app1)
    err_msg = "'app' directory is required but not found"
    assert str(exc_info.value) == err_msg
        

def test_requires_modules_dir_in_project(route_manager, app1, project1):    
    app_dir = project1 / 'app'
    app_dir.mkdir()

    with pytest.raises(exc.InvalidProjectStructure) as exc_info:
        route_manager.init_app(app1)
    err_msg = "'modules' directory is required but not found"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def project2(project1):
    """project with app and modules dirs"""
    (project1 / 'app').mkdir()
    (project1 / 'modules').mkdir()
    yield project1
    for name in list(sys.modules):
        if name.startswith('modules'):
            sys.modules.pop(name)


@pytest.mark.usefixtures('project2')
def test_requires_project_name_in_config(app1, route_manager):    
    app1.config = {'PIGAL_PROJECT_VERSION': '1.0'}
    
    with pytest.raises(exc.InvalidProjectConfig) as exc_info:
        route_manager.init_app(app1)
    err_msg = "Configuration parameter 'PIGAL_PROJECT_NAME' is missing"
    assert str(exc_info.value) == err_msg


@pytest.mark.usefixtures('project2')
def test_requires_project_version_in_config(app1, route_manager):
    app1.config = {'PIGAL_PROJECT_NAME': 'test'}

    with pytest.raises(exc.InvalidProjectConfig) as exc_info:
        route_manager.init_app(app1)
    err_msg = "Configuration parameter 'PIGAL_PROJECT_VERSION' is missing"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app2(app1):
    """app with minimal config"""
    app = app1
    app.config = {
        'PIGAL_PROJECT_NAME': 'demo',
        'PIGAL_PROJECT_VERSION': '0.1'
    }
    return app


@pytest.mark.usefixtures('project2')
def test_create_default_rest_api(app2, route_manager):
    bp_name = ext.__name__
    route_manager.init_app(app2)

    rest_api = ext.Api.return_value
    api_bp = ext.Blueprint.return_value
    ext.Blueprint.assert_called_with('api', bp_name, url_prefix='/api')
    ext.Api.assert_called_with(api_bp, title='demo API', version='0.1')
    app2.register_blueprint.assert_any_call(api_bp)
    assert route_manager.api == rest_api


@pytest.fixture
def project3(project2):
    """project with private and public demo pages"""
    (project2 / 'modules/demo/pages').mkdir(parents=True)
    (project2 / 'modules/_demo/pages').mkdir(parents=True)
    return project2


UI_CODE = """
    \nfrom pigal_flask import ModuleUi
    \nui = ModuleUi(__name__)
    """


def test_register_module_ui_as_blueprint(app2, project3, route_manager):
    routes_file = project3 / 'modules/demo/pages/routes.py'
    routes_file.write_text(UI_CODE, encoding='utf-8')
    route_manager.init_app(app2)

    ui = pkg.ModuleUi.return_value
    app2.register_blueprint.assert_any_call(ui, url_prefix='/demo')


def test_ignore_private_module_ui(app2, project3, route_manager):
    routes_file = project3 / 'modules/_demo/pages/routes.py'
    routes_file.write_text(UI_CODE, encoding='utf-8')
    route_manager.init_app(app2)

    with pytest.raises(AssertionError):
        ui = pkg.ModuleUi.return_value
        app2.register_blueprint.assert_any_call(ui, url_prefix='/_demo')


def test_ignore_invalid_module_ui(app2, project3, route_manager):
    routes_file = project3 / 'modules/demo/pages/routes.py'
    routes_file.write_text("ui = object()", encoding='utf-8')

    with pytest.raises(exc.InvalidModuleUi) as exc_info:
        route_manager.init_app(app2)
    err_msg = "The object 'ui' of modules.demo.pages.routes"
    err_msg += " is not an instance of ModuleUi"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def project4(project2):
    """project with private and public demo services"""
    (project2 / 'modules/demo/services').mkdir(parents=True)
    (project2 / 'modules/_demo/services').mkdir(parents=True)
    return project2


API_CODE = '''
    \nfrom pigal_flask import ModuleApi
    \napi = ModuleApi(__file__)
    '''

def test_register_module_api_as_namespace(app2, project4, route_manager):
    routes_file = project4 / 'modules/demo/services/routes.py'
    routes_file.write_text(API_CODE, encoding='utf-8')
    route_manager.init_app(app2)

    module_api = pkg.ModuleApi.return_value
    rest_api = ext.Api.return_value
    rest_api.add_namespace.assert_any_call(module_api)


def test_ignore_private_module_api(app2, project4, route_manager):
    routes_file = project4 / 'modules/_demo/services/routes.py'
    routes_file.write_text(API_CODE, encoding='utf-8')
    route_manager.init_app(app2)

    with pytest.raises(AssertionError):
        module_api = pkg.ModuleApi.return_value
        rest_api = ext.Api.return_value
        rest_api.add_namespace.assert_any_call(module_api)


def test_ignore_invalid_module_api(app2, project4, route_manager):
    routes_file = project4 / 'modules/demo/services/routes.py'
    routes_file.write_text("api = object()", encoding='utf-8')

    with pytest.raises(exc.InvalidApi) as exc_info:
        route_manager.init_app(app2)
    err_msg = "The object 'api' of modules.demo.services.routes"
    err_msg += " is not an instance of ModuleApi"
    assert str(exc_info.value) == err_msg


