
import os
import tempfile
import pytest
from flask import Flask
from pigal_flask.extensions import Pigal, InvalidProjectStructure


@pytest.fixture
def app1():
    """Flask app for testing"""
    with tempfile.TemporaryDirectory() as tempdir:
        appdir = os.path.join(tempdir)
        app = Flask(__name__, 
                    instance_path=appdir, 
                    instance_relative_config=True)
        yield app

def test_checks_app_directory_in_project_directory(app1):
    app = app1
    with pytest.raises(InvalidProjectStructure) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "'app' directory is required but not found"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app2():
    """Flask app without pages directory"""
    with tempfile.TemporaryDirectory() as tempdir:
        appdir = os.path.join(tempdir, 'app')
        app = Flask(__name__, 
                    instance_path=appdir, 
                    instance_relative_config=True)
        os.makedirs(os.path.join(tempdir, 'services'))
        os.makedirs(appdir)
        yield app
        
def test_checks_pages_directory_in_project_directory(app2):
    app = app2
    with pytest.raises(InvalidProjectStructure) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "'pages' directory is required but not found"
    assert str(exc_info.value) == err_msg


@pytest.fixture
def app3():
    """Flask app without services directory"""
    with tempfile.TemporaryDirectory() as tempdir:
        appdir = os.path.join(tempdir, 'app')
        app = Flask(__name__, 
                    instance_path=appdir, 
                    instance_relative_config=True)
        os.makedirs(os.path.join(tempdir, 'pages'))
        os.makedirs(appdir)
        yield app
        
def test_checks_services_directory_in_project_directory(app3):
    app = app3
    with pytest.raises(InvalidProjectStructure) as exc_info:
        pigal = Pigal()
        pigal.init_app(app)
    err_msg = "'services' directory is required but not found"
    assert str(exc_info.value) == err_msg

