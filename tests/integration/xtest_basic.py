
import os
import sys
import pytest
from flask import Flask
from pigal_flask import Pigal


@pytest.fixture
def project1(app):
    """Flask app without pages and services"""
    # make project structure
    project_dir = app.project_dir
    services_dir = project_dir / 'services'
    services_dir.mkdir()
    pages_dir = project_dir / 'pages'
    pages_dir.mkdir()

    # configure app
    app.config['PIGAL_PROJECT_NAME'] = 'demo'
    app.config['PIGAL_PROJECT_VERSION'] = '0.1'

    # init pigal extension
    pigal = Pigal()
    pigal.init_app(app)


def test_has_no_default_index_page(client, project1):
    response = client.get('/')
    assert response.status_code == 404

def test_has_default_api_doc(client, project1):
    response = client.get('/api/')
    assert response.status_code == 200
    assert 'demo API' in response.data.decode()
        

@pytest.fixture
def project2(app):
    """Flask app with pages only"""
    # make project structure
    project_dir = app.project_dir
    services_dir = project_dir / 'services'
    services_dir.mkdir()
    pages_dir = project_dir / 'pages'
    pages_dir.mkdir()

    # include in PYTHONPATH
    project_path = project_dir.strpath
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
            \n    return 'This is {name}'
            """, encoding='utf-8')

    # create app
    app.config['PIGAL_PROJECT_NAME'] = 'demo'
    app.config['PIGAL_PROJECT_VERSION'] = '0.1'

    # init pigal extension
    pigal = Pigal()
    pigal.init_app(app)
    return app


def test_renders_all_pages_ui(client, project2):
    for name in ('demo1', 'demo2'):
        response = client.get(f'/{name}/')
        assert response.status_code == 200
        assert response.data.decode() == f'This is {name}'
            

@pytest.fixture
def project3(app):
    """Flask app with services only"""
    # make project structure
    project_dir = app.project_dir
    services_dir = project_dir / 'services'
    services_dir.mkdir()
    pages_dir = project_dir / 'pages'
    pages_dir.mkdir()

    # include in PYTHONPATH
    project_path = project_dir.strpath
    if project_path not in sys.path:
        sys.path.append(project_path)

    # create services
    for name in ('demo_v1', 'demo_v2'):
        service_dir = services_dir / name
        service_dir.mkdir()
        routes = service_dir / 'routes.py'
        routes.write_text("""
            \nfrom flask_restx import Resource
            \nfrom pigal_flask.utils import PigalApi
            \napi = PigalApi(__file__)
            \n@api.route('/')
            \nclass HelloApi(Resource):
            \n    def get(self):
            \n        return {'message': 'Hello, World!'}
            """, encoding='utf-8')

    # create app
    app.config['PIGAL_PROJECT_NAME'] = 'demo'
    app.config['PIGAL_PROJECT_VERSION'] = '0.1'

    # init pigal extension
    pigal = Pigal()
    pigal.init_app(app)
    return app


def test_provides_all_services_api(client, project3):
    for url in ('/api/demo/v1/', '/api/demo/v2/'):
        response = client.get(url)
        assert response.status_code == 200
        assert response.json == {'message': 'Hello, World!'}

