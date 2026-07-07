
import os
import sys

import pytest
from flask import Flask, Blueprint
from flask_restx import Api, Namespace

from pigal_flask import utils
from pigal_flask import views
from pigal_flask.extensions import Pigal
from pigal_flask.exceptions import (
    InvalidUi, 
    InvalidApi,
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
    err_msg = "'app' directory is required but not found"
    app = app1
    pigal = Pigal()

    with pytest.raises(InvalidProjectStructure) as exc_info:
        pigal.init_app(app)
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app2(tmpdir):
    """Flask app without modules directory"""
    app_dir = tmpdir / 'app'
    app_dir.mkdir()
    return Flask(__name__, 
                instance_path=app_dir, 
                instance_relative_config=True)
        

def test_checks_modules_directory_in_project_directory(app2):
    err_msg = "'modules' directory is required but not found"
    app = app2
    pigal = Pigal()

    with pytest.raises(InvalidProjectStructure) as exc_info:
        pigal.init_app(app)
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app4(app2, tmpdir):
    """Flask app with modules directory"""
    project_path = tmpdir.strpath
    if project_path not in sys.path:
        sys.path.append(project_path)
    modules_dir = tmpdir / 'modules'
    modules_dir.mkdir()
    app2.modules_dir = modules_dir
    return app2


def test_requires_project_name_in_app_config(app4):
    err_msg = "Configuration parameter 'PIGAL_PROJECT_NAME' is missing"
    app = app4
    pigal = Pigal()
    
    with pytest.raises(InvalidProjectConfig) as exc_info:
        pigal.init_app(app)
    assert str(exc_info.value) == err_msg


def test_requires_project_version_in_app_config(app4):
    err_msg = "Configuration parameter 'PIGAL_PROJECT_VERSION' is missing"
    pigal = Pigal()
    app = app4
    app.config['PIGAL_PROJECT_NAME'] = 'test'

    with pytest.raises(InvalidProjectConfig) as exc_info:
        pigal.init_app(app)
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app5(app4):
    """Flask app with minimal config"""
    app4.config['PIGAL_PROJECT_NAME'] = 'demo'
    app4.config['PIGAL_PROJECT_VERSION'] = '0.1'
    return app4


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


def test_has_no_default_index_frontend(app5):
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


class FakeUi(Blueprint):
    def __init__(self, file):
        dir_ = os.path.dirname(file)
        name = os.path.basename(dir_)
        super().__init__(name, f'modules.{name}.views')


@pytest.fixture
def app6(app5, monkeypatch):
    """Flask app with pigal modules"""
    monkeypatch.setattr(views, 'WebUi', FakeUi)
    modules_dir = app5.modules_dir
    for name in ('demo1', 'demo2', '_demo3'):
        module_dir = modules_dir / name
        module_dir.mkdir()
        code = f"""
            \nfrom pigal_flask import views
            \nui = views.WebUi(__file__)
            """
        views_file = module_dir / 'views.py'
        views_file.write_text(code, encoding='utf-8')
    return app5


def test_registers_web_ui_as_blueprint(app6):
    app = app6
    pigal = Pigal()
    pigal.init_app(app)

    blueprints = app.blueprints
    assert 'demo1' in blueprints
    assert 'demo2' in blueprints
    assert isinstance(blueprints['demo1'], FakeUi)
    assert isinstance(blueprints['demo2'], FakeUi)


def test_ignores_private_directories_within_modules_directory(app6):
    app = app6
    pigal = Pigal()
    pigal.init_app(app)

    assert '_demo3' not in app.blueprints


# def test_renders_all_web_ui(app6):
#     app = app6
#     pigal = Pigal()
#     pigal.init_app(app)

#     with app.test_client() as client:
#         for name in ('demo1', 'demo2'):
#             response = client.get(f'/{name}/')
#             assert response.status_code == 200
#             assert response.data.decode() == f'This is {name}'


@pytest.fixture
def app7(app5, monkeypatch):
    """Flask app with incorrect modules ui"""
    monkeypatch.setattr(views, 'WebUi', FakeUi)
    modules_dir = app5.modules_dir
    module_dir = modules_dir / 'demo'
    module_dir.mkdir()
    code = f"""ui = object()"""    
    views_file = module_dir / 'views.py'
    views_file.write_text(code, encoding='utf-8')
    return app5


def test_checks_module_ui_is_web_ui_instance(app7):
    err_msg = "The object 'ui' of module 'demo' "
    err_msg += "is not an instance of 'WebUi'"
    app = app7
    pigal = Pigal()

    with pytest.raises(InvalidUi) as exc_info:
        pigal.init_app(app)
    assert str(exc_info.value) == err_msg
    assert 'demo' not in app.blueprints


class FakePigalApi(Namespace):
    def __init__(self, file):
        dir_ = os.path.dirname(file)
        name = os.path.basename(dir_)
        super().__init__(name, path=f'/fake/{name}')


@pytest.fixture
def app8(app5, monkeypatch):
    """Flask app with pigal modules"""
    monkeypatch.setattr(utils, 'PigalApi', FakePigalApi)
    modules_dir = app5.modules_dir
    for name in ('demo_v1', 'demo_v2', '_demo_v3'):
        backend_dir = modules_dir / name
        backend_dir.mkdir()
        code = """
            \nfrom flask_restx import Resource
            \nfrom pigal_flask.utils import PigalApi
            \napi = PigalApi(__file__)
            \n@api.route('/')
            \nclass HelloApi(Resource):
            \n    def get(self):
            \n        return {'message': 'Hello, World!'}
            """
        routes = backend_dir / 'routes.py'
        routes.write_text(code, encoding='utf-8')
    return app5


def test_registers_modules_api_as_namespace(app8):
    app = app8
    pigal = Pigal()
    pigal.init_app(app)

    namespaces = {n.name:n for n in pigal.api.namespaces}
    assert 'demo_v1' in namespaces
    assert 'demo_v2' in namespaces
    assert isinstance(namespaces['demo_v1'], FakePigalApi)
    assert isinstance(namespaces['demo_v2'], FakePigalApi)


def test_ignores_private_directories_within_modules_directory(app8):
    app = app8
    pigal = Pigal()
    pigal.init_app(app)

    namespaces = {n.name:n for n in pigal.api.namespaces}
    assert '_demo_v3' not in namespaces


def test_provides_all_modules_api(app8):
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
    """Flask app with incorrect modules api"""
    monkeypatch.setattr(utils, 'PigalApi', FakePigalApi)
    modules_dir = app5.modules_dir
    backend_dir = modules_dir / 'demo_v0'
    backend_dir.mkdir()
    code = f"""
        \nimport pigal_flask.utils as utl
        \napi = object()
        """    
    routes = backend_dir / 'routes.py'
    routes.write_text(code, encoding='utf-8')
    return app5


def test_checks_backend_api_is_pigal_api_instance(app9):
    err_msg = "The object 'api' of backend 'demo_v0' "
    err_msg += "is not an instance of 'PigalApi'"
    app = app9
    pigal = Pigal()

    with pytest.raises(InvalidApi) as exc_info:
        pigal.init_app(app)
    assert str(exc_info.value) == err_msg
    assert 'demo' not in app.blueprints

