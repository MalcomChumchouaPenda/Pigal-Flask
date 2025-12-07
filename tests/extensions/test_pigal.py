
import sys
import pytest
from flask import Flask
from pigal_flask.extensions import Pigal, InvalidProjectStructure


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
    project_path = app2.project_dir.strpath
    if project_path not in sys.path:
        sys.path.append(project_path)
    return app2

@pytest.fixture
def project3(app3):
    """Complete project"""
    services_dir = app3.project_dir / 'services'
    services_dir.mkdir()
    pages_dir = app3.project_dir / 'pages'
    pages_dir.mkdir()
    for name in ('demo1', 'demo2'):
        page_dir = pages_dir / name
        page_dir.mkdir()
        code = f"""
            \nfrom pigal_flask import PigalUi
            \nui = PigalUi(__file__)
            \n@ui.route('/')
            \ndef index():
            \n\treturn 'This is {name}'
            """    
        routes = page_dir / 'routes.py'
        routes.write_text(code, encoding='utf-8')


def test_registers_pages_ui_as_blueprint(app3, project3):
    app = app3
    pigal = Pigal()
    pigal.init_app(app)
    assert 'demo1' in app.blueprints
    assert 'demo2' in app.blueprints

def test_registers_pages_ui_with_url_prefix(app3, project3):
    app = app3
    pigal = Pigal()
    pigal.init_app(app)
    with app.test_client() as client:
        for name in ('demo1', 'demo2'):
            response = client.get(f'/{name}/')
            assert response.data.decode() == f'This is {name}'
            assert response.status_code == 200


@pytest.fixture
def project4(app3):
    """Project with private directories"""
    services_dir = app3.project_dir / 'services'
    services_dir.mkdir()
    pages_dir = app3.project_dir / 'pages'
    pages_dir.mkdir()
    for name in ('_demo1', '__demo2'):
        page_dir = pages_dir / name
        page_dir.mkdir()
        code = f"""
            \nfrom pigal_flask import PigalUi
            \nui = PigalUi(__file__)
            """    
        routes = page_dir / 'routes.py'
        routes.write_text(code, encoding='utf-8')


def test_ignores_private_directories_within_pages_directory(app3, project4):
    app = app3
    pigal = Pigal()
    pigal.init_app(app)
    assert '_demo1' not in app.blueprints
    assert '__demo2' not in app.blueprints

