
import os
import sys

import pytest
from mock import MagicMock
from flask import Flask, Blueprint
from flask_restx import Api

from pigal_flask import utils
from pigal_flask.extensions import (
    Pigal, 
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


class FakePigalUi(Blueprint):
    def __init__(self, file):
        dir_ = os.path.dirname(file)
        name = os.path.basename(dir_)
        super().__init__(name, f'pages.{name}.routes')

@pytest.fixture
def app6(app5, monkeypatch):
    """Flask app with pigal pages"""
    app = app5
    pages_dir = app.pages_dir
    for name in ('demo1', 'demo2', '_demo3'):
        page_dir = pages_dir / name
        page_dir.mkdir()
        code = f"""
            \nfrom pigal_flask.utils import PigalUi
            \nui = PigalUi(__file__)
            """    
        routes = page_dir / 'routes.py'
        routes.write_text(code, encoding='utf-8')
    monkeypatch.setattr(utils, 'PigalUi', FakePigalUi)
    return app

def test_registers_pages_ui_as_blueprint(app6):
    app = app6
    pigal = Pigal()
    pigal.init_app(app)
    assert 'demo1' in app.blueprints
    assert 'demo2' in app.blueprints

def test_ignores_private_directories_within_pages_directory(app6):
    app = app6
    pigal = Pigal()
    pigal.init_app(app)
    assert '_demo3' not in app.blueprints


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