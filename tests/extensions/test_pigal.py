
import pytest
from flask import Flask
from pigal_flask.extensions import Pigal, InvalidProjectStructure


@pytest.fixture
def app1(tmpdir):
    """Flask app for testing"""
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

