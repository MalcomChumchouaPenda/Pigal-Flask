
import os
import sys
import shutil

import pytest
from flask import Flask, Blueprint
from flask_restx import Api, Namespace

from pigal_flask import utils
from pigal_flask import views
# from pigal_flask import extensions as pkg
from pigal_flask.extensions import Pigal
from pigal_flask.exceptions import (
    InvalidUi, 
    InvalidApi,
    InvalidProjectStructure,
    InvalidProjectConfig
)


def create_app(project_dir):
    return Flask(__name__, 
                instance_path=str(project_dir / 'app.py'), 
                instance_relative_config=True)

    
@pytest.fixture
def project_dir(tmpdir_factory):
    fake_dir = tmpdir_factory.mktemp('fake')
    fake_path = fake_dir.strpath
    if fake_path not in sys.path:
        sys.path.append(fake_path)
    yield fake_dir
    shutil.rmtree(fake_path)
    sys.path.remove(fake_path)


@pytest.fixture
def project_without_app(project_dir):
    modules_dir = project_dir / 'modules'
    modules_dir.mkdir()
    return project_dir


def test_checks_app_dir_in_project_dir(project_without_app):
    err_msg = "'app' directory is required but not found"
    app = create_app(project_without_app)
    pigal = Pigal()

    with pytest.raises(InvalidProjectStructure) as exc_info:
        pigal.init_app(app)
    assert str(exc_info.value) == err_msg


@pytest.fixture
def project_without_modules(project_dir):
    app_dir = project_dir / 'app'
    app_dir.mkdir()
    return project_dir
        

def test_checks_modules_dir_in_project_dir(project_without_modules):
    err_msg = "'modules' directory is required but not found"
    app = create_app(project_without_modules)
    pigal = Pigal()

    with pytest.raises(InvalidProjectStructure) as exc_info:
        pigal.init_app(app)
    assert str(exc_info.value) == err_msg


@pytest.fixture
def full_project_dir(project_dir):
    app_dir = project_dir / 'app'
    app_dir.mkdir()
    modules_dir = project_dir / 'modules'
    modules_dir.mkdir()
    yield project_dir
    for name in list(sys.modules):
        if name.startswith('modules'):
            sys.modules.pop(name)


@pytest.fixture
def app_with_no_config(full_project_dir):
    return create_app(full_project_dir)


def test_requires_project_name_in_app_config(app_with_no_config):
    err_msg = "Configuration parameter 'PIGAL_PROJECT_NAME' is missing"
    pigal = Pigal()
    app = app_with_no_config
    app.config['PIGAL_PROJECT_VERSION'] = '1.0'
    
    with pytest.raises(InvalidProjectConfig) as exc_info:
        pigal.init_app(app)
    assert str(exc_info.value) == err_msg


def test_requires_project_version_in_app_config(app_with_no_config):
    err_msg = "Configuration parameter 'PIGAL_PROJECT_VERSION' is missing"
    pigal = Pigal()
    app = app_with_no_config
    app.config['PIGAL_PROJECT_NAME'] = 'test'

    with pytest.raises(InvalidProjectConfig) as exc_info:
        pigal.init_app(app)
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app_with_config(full_project_dir):
    app = create_app(full_project_dir)
    app.config['PIGAL_PROJECT_NAME'] = 'demo'
    app.config['PIGAL_PROJECT_VERSION'] = '0.1'
    return app


def test_create_a_default_rest_api(app_with_config):
    app = app_with_config
    pigal = Pigal()
    pigal.init_app(app)

    assert isinstance(pigal.api, Api)
    assert pigal.api.title == app.config['PIGAL_PROJECT_NAME'] + ' API'
    assert pigal.api.version == app.config['PIGAL_PROJECT_VERSION']


def test_create_an_api_blueprint(app_with_config):
    app = app_with_config
    pigal = Pigal()
    pigal.init_app(app)

    assert pigal.api.app == app.blueprints['api']
    assert pigal.api.app.url_prefix == '/api'


def test_has_no_default_index_frontend(app_with_config):
    app = app_with_config
    pigal = Pigal()
    pigal.init_app(app)

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 404


def test_has_default_api_doc(app_with_config):
    app = app_with_config
    pigal = Pigal()
    pigal.init_app(app)

    with app.test_client() as client:
        response = client.get('/api/')
        assert response.status_code == 200
        assert 'demo API' in response.data.decode()
        assert 'swagger' in response.data.decode()


@pytest.fixture
def ui_cls(monkeypatch):
    import pigal_flask as pkg1
    import pigal_flask.extensions as pkg2

    class FakeUi(Blueprint):
        def __init__(self, file):
            dir_ = os.path.dirname(file)
            name = os.path.basename(dir_)
            super().__init__(name, f'modules.{name}.views')

    monkeypatch.setattr(pkg1, 'ModuleUi', FakeUi)
    monkeypatch.setattr(pkg2, 'ModuleUi', FakeUi)
    return FakeUi


VIEWS_CODE = """
    \nfrom pigal_flask import ModuleUi
    \nui = ModuleUi(__file__)
    """


@pytest.fixture
def demos_with_views(full_project_dir):
    created = []
    modules_dir = full_project_dir / 'modules'
    for name in ('demo1', 'demo2', '_demo3'):
        module_dir = modules_dir / name
        module_dir.mkdir()
        views_file = module_dir / 'views.py'
        views_file.write_text(VIEWS_CODE, encoding='utf-8')
        created.append(module_dir)
    return created


@pytest.mark.usefixtures('demos_with_views')
def test_registers_web_ui_as_blueprint(app_with_config, ui_cls):
    app = app_with_config
    pigal = Pigal()
    pigal.init_app(app)

    blueprints = app.blueprints
    assert 'demo1' in blueprints
    assert 'demo2' in blueprints
    assert isinstance(blueprints['demo1'], ui_cls)
    assert isinstance(blueprints['demo2'], ui_cls)


@pytest.mark.usefixtures('demos_with_views', 'ui_cls')
def test_ignores_private_dirs_within_modules_dir(app_with_config):
    app = app_with_config
    pigal = Pigal()
    pigal.init_app(app)
    assert '_demo3' not in app.blueprints


@pytest.fixture
def demo_with_bad_views(full_project_dir):
    module_dir = full_project_dir / 'modules' / 'demo'
    module_dir.mkdir()
    views_file = module_dir / 'views.py'
    views_file.write_text("ui = object()", encoding='utf-8')
    return module_dir


@pytest.mark.usefixtures('demo_with_bad_views', 'ui_cls')
def test_checks_module_ui_is_web_ui(app_with_config):
    err_msg = "The object 'ui' of modules.demo.views "
    err_msg += "is not an instance of ModuleUi"
    app = app_with_config
    pigal = Pigal()

    with pytest.raises(InvalidUi) as exc_info:
        pigal.init_app(app)
    assert str(exc_info.value) == err_msg



@pytest.fixture
def api_cls(monkeypatch):
    import pigal_flask as pkg1
    import pigal_flask.extensions as pkg2

    class FakeApi(Namespace):
        def __init__(self, file):
            dir_ = os.path.dirname(file)
            name = os.path.basename(dir_)
            super().__init__(name, path=f'/{name}')

    monkeypatch.setattr(pkg1, 'ModuleApi', FakeApi)
    monkeypatch.setattr(pkg2, 'ModuleApi', FakeApi)
    return FakeApi


SERVICES_CODE = '''
    \nfrom pigal_flask import ModuleApi
    \napi = ModuleApi(__file__)
    '''


@pytest.fixture
def demos_with_services(full_project_dir):
    modules_dir = full_project_dir / 'modules'
    created = []
    for name in ('demo1', 'demo2', '_demo3'):
        module_dir = modules_dir / name
        module_dir.mkdir()
        services_file = module_dir / 'services.py'
        services_file.write_text(SERVICES_CODE, encoding='utf-8')
        created.append(module_dir)
    return created


@pytest.mark.usefixtures('demos_with_services')
def test_registers_modules_api_as_namespace(app_with_config, api_cls):
    app = app_with_config
    pigal = Pigal()
    pigal.init_app(app)

    namespaces = {n.name:n for n in pigal.api.namespaces}
    assert 'demo1' in namespaces
    assert 'demo2' in namespaces
    assert isinstance(namespaces['demo1'], api_cls)
    assert isinstance(namespaces['demo2'], api_cls)


@pytest.mark.usefixtures('demos_with_services', 'api_cls')
def test_ignores_private_dirs_within_modules_dir(app_with_config):
    app = app_with_config
    pigal = Pigal()
    pigal.init_app(app)

    namespaces = {n.name:n for n in pigal.api.namespaces}
    assert '_demo3' not in namespaces


@pytest.fixture
def demo_with_bad_services(full_project_dir):
    module_dir = full_project_dir / 'modules' / 'demo'
    module_dir.mkdir()
    services_file = module_dir / 'services.py'
    services_file.write_text('api = object()', encoding='utf-8')
    return module_dir


@pytest.mark.usefixtures('demo_with_bad_services', 'api_cls')
def test_checks_module_api_is_pigal_api_instance(app_with_config):
    err_msg = "The object 'api' of modules.demo.services "
    err_msg += "is not an instance of ModuleApi"
    app = app_with_config
    pigal = Pigal()

    with pytest.raises(InvalidApi) as exc_info:
        pigal.init_app(app)
    assert str(exc_info.value) == err_msg
    assert 'demo' not in app.blueprints


RESOURCES_CODE = """
    \nfrom flask_restx import Resource
    \nfrom .services import api

    \n@api.route('/')
    \nclass HelloApi(Resource):
    \n    def get(self):
    \n        return {'message': 'Hello, World!'}
    """


@pytest.fixture
def demo_with_resources(full_project_dir):
    module_dir = full_project_dir / 'modules' / 'demo'
    module_dir.mkdir()
    services_file = module_dir / 'services.py'
    services_file.write_text(SERVICES_CODE, encoding='utf-8')   
    resources_file = module_dir / 'resources.py'
    resources_file.write_text(RESOURCES_CODE, encoding='utf-8')  
    return module_dir


@pytest.mark.usefixtures('demo_with_resources', 'api_cls')
def test_provides_all_modules_api(app_with_config):
    app = app_with_config
    pigal = Pigal()
    pigal.init_app(app)

    with app.test_client() as client:
        response = client.get('/api/demo/')
        assert response.status_code == 200
        assert response.json == {'message': 'Hello, World!'}
