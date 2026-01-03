
import os
import sys

import pytest
from flask import Flask, Blueprint
from flask_restx import Api, Namespace

from pigal_flask import utils
from pigal_flask.extensions import Pigal
from pigal_flask.exceptions import (
    InvalidPageUi, 
    InvalidServiceApi,
    InvalidProjectStructure,
    InvalidProjectConfig
)


@pytest.fixture
def app1(tmpdir):
    """Flask app created outside app directory"""
    return Flask(__name__, 
                instance_path=tmpdir.strpath, 
                instance_relative_config=True)

def test_checks_app_directory_in_project_directory(app1):
    app = app1
    with pytest.raises(InvalidProjectStructure) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "'app' directory is required but not found"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app2(tmpdir):
    """Flask app without pages directory"""
    services_dir = tmpdir / 'services'
    services_dir.mkdir()
    app_dir = tmpdir / 'app'
    app_dir.mkdir()
    return Flask(__name__, 
                instance_path=app_dir, 
                instance_relative_config=True)
        
def test_checks_pages_directory_in_project_directory(app2):
    app = app2
    with pytest.raises(InvalidProjectStructure) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "'pages' directory is required but not found"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app3(tmpdir):
    """Flask app without services directory"""
    pages_dir = tmpdir / 'pages'
    pages_dir.mkdir()
    app_dir = tmpdir / 'app'
    app_dir.mkdir()
    return Flask(__name__, 
                instance_path=app_dir, 
                instance_relative_config=True)

def test_checks_services_directory_in_project_directory(app3):
    app = app3
    with pytest.raises(InvalidProjectStructure) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "'services' directory is required but not found"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app4(tmpdir):
    """Flask app with pages and services directory"""
    project_path = tmpdir.strpath
    if project_path not in sys.path:
        sys.path.append(project_path)
    services_dir = tmpdir / 'services'
    services_dir.mkdir()
    pages_dir = tmpdir / 'pages'
    pages_dir.mkdir()
    app_dir = tmpdir / 'app'
    app_dir.mkdir()
    app = Flask(__name__, 
                instance_path=app_dir, 
                instance_relative_config=True)
    app.pages_dir = pages_dir
    app.services_dir = services_dir
    return app

def test_requires_project_name_in_app_config(app4):
    app = app4
    with pytest.raises(InvalidProjectConfig) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "Configuration parameter 'PIGAL_PROJECT_NAME' is missing"
    assert str(exc_info.value) == err_msg

def test_requires_project_version_in_app_config(app4):
    app = app4
    app.config['PIGAL_PROJECT_NAME'] = 'test'
    with pytest.raises(InvalidProjectConfig) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "Configuration parameter 'PIGAL_PROJECT_VERSION' is missing"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app5(app4):
    """Flask app with minimal config"""
    app = app4
    app.config['PIGAL_PROJECT_NAME'] = 'demo'
    app.config['PIGAL_PROJECT_VERSION'] = '0.1'
    return app

def test_create_a_default_rest_api(app5):
    app = app5
    pigal = Pigal()
    pigal.init_app(app)
    assert isinstance(pigal.api, Api)
    assert pigal.api.title == app.config['PIGAL_PROJECT_NAME'] + ' API'
    assert pigal.api.version == app.config['PIGAL_PROJECT_VERSION']

def test_create_an_api_blueprint(app5):
    app = app5
    pigal = Pigal()
    pigal.init_app(app)
    assert pigal.api.app == app.blueprints['api']
    assert pigal.api.app.url_prefix == '/api'

def test_has_no_default_index_page(app5):
    app = app5
    pigal = Pigal()
    pigal.init_app(app)
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 404

def test_has_default_api_doc(app5):
    app = app5
    pigal = Pigal()
    pigal.init_app(app)
    with app.test_client() as client:
        response = client.get('/api/')
        assert response.status_code == 200
        assert 'demo API' in response.data.decode()
        assert 'swagger' in response.data.decode()


class FakePigalUi(Blueprint):
    def __init__(self, file):
        dir_ = os.path.dirname(file)
        name = os.path.basename(dir_)
        super().__init__(name, f'pages.{name}.routes')

@pytest.fixture
def app6(app5, monkeypatch):
    """Flask app with pigal pages"""
    monkeypatch.setattr(utils, 'PigalUi', FakePigalUi)
    app = app5
    pages_dir = app.pages_dir
    for name in ('demo1', 'demo2', '_demo3'):
        page_dir = pages_dir / name
        page_dir.mkdir()
        code = f"""
            \nimport pigal_flask.utils as utl
            \nui = utl.PigalUi(__file__)
            \n@ui.route('/')
            \ndef index():
            \n    return 'This is {name}'
            """
        routes = page_dir / 'routes.py'
        routes.write_text(code, encoding='utf-8')
    return app

def test_registers_pages_ui_as_blueprint(app6):
    app = app6
    pigal = Pigal()
    pigal.init_app(app)
    blueprints = app.blueprints
    assert 'demo1' in blueprints
    assert 'demo2' in blueprints
    assert isinstance(blueprints['demo1'], FakePigalUi)
    assert isinstance(blueprints['demo2'], FakePigalUi)

def test_ignores_private_directories_within_pages_directory(app6):
    app = app6
    pigal = Pigal()
    pigal.init_app(app)
    assert '_demo3' not in app.blueprints

def test_renders_all_pages_ui(app6):
    app = app6
    pigal = Pigal()
    pigal.init_app(app)
    with app.test_client() as client:
        for name in ('demo1', 'demo2'):
            response = client.get(f'/{name}/')
            assert response.status_code == 200
            assert response.data.decode() == f'This is {name}'


@pytest.fixture
def app7(app5, monkeypatch):
    """Flask app with incorrect pages ui"""
    monkeypatch.setattr(utils, 'PigalUi', FakePigalUi)
    app = app5
    pages_dir = app.pages_dir
    page_dir = pages_dir / 'demo'
    page_dir.mkdir()
    code = f"""
        \nimport pigal_flask.utils as utl
        \nui = object()
        """    
    routes = page_dir / 'routes.py'
    routes.write_text(code, encoding='utf-8')
    return app

def test_checks_page_ui_is_pigal_ui_instance(app7):
    app = app7
    with pytest.raises(InvalidPageUi) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "The object 'ui' of page 'demo' "
    err_msg += "is not an instance of 'PigalUi'"
    assert str(exc_info.value) == err_msg
    assert 'demo' not in app.blueprints


class FakePigalApi(Namespace):
    def __init__(self, file):
        dir_ = os.path.dirname(file)
        name = os.path.basename(dir_)
        super().__init__(name, path=f'/fake/{name}')

@pytest.fixture
def app8(app5, monkeypatch):
    """Flask app with pigal services"""
    monkeypatch.setattr(utils, 'PigalApi', FakePigalApi)
    app = app5
    services_dir = app.services_dir
    for name in ('demo_v1', 'demo_v2', '_demo_v3'):
        service_dir = services_dir / name
        service_dir.mkdir()
        code = """
            \nfrom flask_restx import Resource
            \nfrom pigal_flask.utils import PigalApi
            \napi = PigalApi(__file__)
            \n@api.route('/')
            \nclass HelloApi(Resource):
            \n    def get(self):
            \n        return {'message': 'Hello, World!'}
            """
        routes = service_dir / 'routes.py'
        routes.write_text(code, encoding='utf-8')
    return app

def test_registers_services_api_as_namespace(app8):
    app = app8
    pigal = Pigal()
    pigal.init_app(app)
    namespaces = {n.name:n for n in pigal.api.namespaces}
    assert 'demo_v1' in namespaces
    assert 'demo_v2' in namespaces
    assert isinstance(namespaces['demo_v1'], FakePigalApi)
    assert isinstance(namespaces['demo_v2'], FakePigalApi)

def test_ignores_private_directories_within_services_directory(app8):
    app = app8
    pigal = Pigal()
    pigal.init_app(app)
    namespaces = {n.name:n for n in pigal.api.namespaces}
    assert '_demo_v3' not in namespaces

def test_provides_all_services_api(app8):
    app = app8
    pigal = Pigal()
    pigal.init_app(app)
    with app.test_client() as client:
        for url in ('/api/fake/demo_v1/', '/api/fake/demo_v2/'):
            response = client.get(url)
            assert response.status_code == 200
            assert response.json == {'message': 'Hello, World!'}


@pytest.fixture
def app9(app5, monkeypatch):
    """Flask app with incorrect services api"""
    monkeypatch.setattr(utils, 'PigalApi', FakePigalApi)
    app = app5
    services_dir = app.services_dir
    service_dir = services_dir / 'demo_v0'
    service_dir.mkdir()
    code = f"""
        \nimport pigal_flask.utils as utl
        \napi = object()
        """    
    routes = service_dir / 'routes.py'
    routes.write_text(code, encoding='utf-8')
    return app

def test_checks_service_api_is_pigal_api_instance(app9):
    app = app9
    with pytest.raises(InvalidServiceApi) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "The object 'api' of service 'demo_v0' "
    err_msg += "is not an instance of 'PigalApi'"
    assert str(exc_info.value) == err_msg
    assert 'demo' not in app.blueprints
