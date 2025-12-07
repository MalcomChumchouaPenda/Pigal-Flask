
import os
import sys

import pytest
from mock import MagicMock
from flask import Flask, Blueprint
from flask_restx import Api

from pigal_flask import utils
from pigal_flask.extensions import Pigal, InvalidProjectStructure, InvalidProjectConfig


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
    """Flask app created inside app directory"""
    app_dir = tmpdir / 'app'
    app_dir.mkdir()
    app = Flask(__name__, 
                instance_path=app_dir, 
                instance_relative_config=True)
    app.project_dir = tmpdir
    return app

@pytest.fixture
def project1(app2):
    """Flask app without pages directory"""
    services_dir = app2.project_dir / 'services'
    services_dir.mkdir()
        

def test_checks_pages_directory_in_project_directory(app2, project1):
    app = app2
    with pytest.raises(InvalidProjectStructure) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "'pages' directory is required but not found"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def project2(app2):
    """Flask app without services directory"""
    pages_dir = app2.project_dir / 'pages'
    pages_dir.mkdir()

        
def test_checks_services_directory_in_project_directory(app2, project2):
    app = app2
    with pytest.raises(InvalidProjectStructure) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "'services' directory is required but not found"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app3(app2):
    """Flask app directory included in PYTHONPATH"""
    app = app2
    project_path = app.project_dir.strpath
    if project_path not in sys.path:
        sys.path.append(project_path)
    services_dir = app.project_dir / 'services'
    services_dir.mkdir()
    pages_dir = app.project_dir / 'pages'
    pages_dir.mkdir()
    app.pages_dir = pages_dir
    app.services_dir = services_dir
    return app

def test_requires_project_name_in_app_config(app3):
    app = app3
    with pytest.raises(InvalidProjectConfig) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "Configuration parameter 'PIGAL_PROJECT_NAME' is missing"
    assert str(exc_info.value) == err_msg

def test_requires_project_version_in_app_config(app3):
    app = app3
    app.config['PIGAL_PROJECT_NAME'] = 'test'
    with pytest.raises(InvalidProjectConfig) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "Configuration parameter 'PIGAL_PROJECT_VERSION' is missing"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app4(app3):
    """Flask app with minimal config"""
    app = app3
    app.config['PIGAL_PROJECT_NAME'] = 'demo'
    app.config['PIGAL_PROJECT_VERSION'] = 'demo'
    return app

@pytest.fixture
def pigal_ui(monkeypatch):
    class PigalUi(Blueprint):
        def __init__(self, file):
            dir_ = os.path.dirname(file)
            name = os.path.basename(dir_)
            super().__init__(name, f'pages.{name}.routes')
    monkeypatch.setattr(utils, 'PigalUi', PigalUi)

@pytest.fixture
def project3(app4, pigal_ui):
    """Complete project"""
    pages_dir = app4.pages_dir
    for name in ('demo1', 'demo2'):
        page_dir = pages_dir / name
        page_dir.mkdir()
        code = f"""
            \nfrom pigal_flask.utils import PigalUi
            \nui = PigalUi(__file__)
            \n@ui.route('/')
            \ndef index():
            \n\treturn 'This is {name}'
            """    
        routes = page_dir / 'routes.py'
        routes.write_text(code, encoding='utf-8')


def test_registers_pages_ui_as_blueprint(app4, project3):
    app = app4
    pigal = Pigal()
    pigal.init_app(app)
    assert 'demo1' in app.blueprints
    assert 'demo2' in app.blueprints

def test_registers_pages_ui_with_url_prefix(app4, project3):
    app = app4
    pigal = Pigal()
    pigal.init_app(app)
    with app.test_client() as client:
        for name in ('demo1', 'demo2'):
            response = client.get(f'/{name}/')
            assert response.data.decode() == f'This is {name}'
            assert response.status_code == 200


@pytest.fixture
def project4(app4, monkeypatch):
    """Project with private directories"""
    monkeypatch.setattr(utils, 'PigalUi', MagicMock())
    monkeypatch.setattr(utils, 'PigalApi', MagicMock())
    pages_dir = app4.pages_dir
    for name in ('_demo1', '__demo2'):
        page_dir = pages_dir / name
        page_dir.mkdir()
        code = f"""
            \nfrom pigal_flask import PigalUi
            \nui = PigalUi(__file__)
            """    
        routes = page_dir / 'routes.py'
        routes.write_text(code, encoding='utf-8')


def test_ignores_private_directories_within_pages_directory(app4, project4):
    app = app4
    pigal = Pigal()
    pigal.init_app(app)
    assert '_demo1' not in app.blueprints
    assert '__demo2' not in app.blueprints


def test_create_a_default_rest_api(app4, project4):
    app = app4
    pigal = Pigal()
    pigal.init_app(app)
    assert isinstance(pigal.api, Api)
    assert pigal.api.title == app.config['PIGAL_PROJECT_NAME'] + ' API'
    assert pigal.api.version == app.config['PIGAL_PROJECT_VERSION']

def test_create_an_api_blueprint(app4, project4):
    app = app4
    pigal = Pigal()
    pigal.init_app(app)
    assert pigal.api.app == app.blueprints['api']
    assert pigal.api.app.url_prefix == '/api'


# @pytest.fixture
# def project5(app4):
#     """Project with services"""
#     services_dir = app4.services_dir
#     for name in ('demo_v1', 'demo_v2'):
#         service_dir = services_dir / name
#         service_dir.mkdir()
#         code = f"""
#             \nfrom pigal_flask import PigalApi
#             \nui = PigalUi(__file__)
#             \n@ui.route('/')
#             \ndef index():
#             \n\treturn 'This is {name}'
#             """    
#         routes = page_dir / 'routes.py'
#         routes.write_text(code, encoding='utf-8')