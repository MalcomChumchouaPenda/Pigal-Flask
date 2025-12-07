
import os
import sys
import pytest
from flask import Flask
from pigal_flask import Pigal


@pytest.fixture
def app1(tmpdir):
    """Flask app without pages and services"""
    # make project structure
    services_dir = tmpdir / 'services'
    services_dir.mkdir()
    pages_dir = tmpdir / 'pages'
    pages_dir.mkdir()
    app_dir = tmpdir / 'app'
    app_dir.mkdir()

    # create app
    app = Flask(__name__, 
                instance_path=app_dir, 
                instance_relative_config=True)
    app.config['PIGAL_PROJECT_NAME'] = 'demo'
    app.config['PIGAL_PROJECT_VERSION'] = '0.1'

    # init pigal extension
    pigal = Pigal()
    pigal.init_app(app)
    return app


def test_has_no_default_index_page(app1):
    with app1.test_client() as client:
        response = client.get('/')
        assert response.status_code == 404

def test_has_default_api_doc(app1):
    with app1.test_client() as client:
        response = client.get('/api/')
        assert response.status_code == 200
        assert 'demo API' in response.data.decode()
        

@pytest.fixture
def app2(tmpdir):
    """Flask app with pages only"""
    # make project structure
    services_dir = tmpdir / 'services'
    services_dir.mkdir()
    pages_dir = tmpdir / 'pages'
    pages_dir.mkdir()
    app_dir = tmpdir / 'app'
    app_dir.mkdir()

    # include in PYTHONPATH
    project_path = tmpdir.strpath
    if project_path not in sys.path:
        sys.path.append(project_path)

    # create pages
    for name in ('demo1', 'demo2'):
        page_dir = pages_dir / name
        page_dir.mkdir()
        routes = page_dir / 'routes.py'
        routes.write_text(f"""
            \nfrom pigal_flask.utils import PigalUi
            \nui = PigalUi(__file__)
            \n@ui.route('/')
            \ndef index():
            \n\treturn 'This is {name}'
            """, encoding='utf-8')

    # create app
    app = Flask(__name__, 
                instance_path=app_dir, 
                instance_relative_config=True)
    app.config['PIGAL_PROJECT_NAME'] = 'demo'
    app.config['PIGAL_PROJECT_VERSION'] = '0.1'

    # init pigal extension
    pigal = Pigal()
    pigal.init_app(app)
    return app


def test_has_render_all_pages_ui(app2):
    with app2.test_client() as client:
        for name in ('demo1', 'demo2'):
            response = client.get(f'/{name}/')
            assert response.status_code == 200
            assert response.data.decode() == f'This is {name}'