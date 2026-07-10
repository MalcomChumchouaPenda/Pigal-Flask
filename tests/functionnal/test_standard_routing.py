
import os
import sys
import pytest
from unittest.mock import MagicMock
from flask import Flask
from flask.views import View, MethodView
from pigal_flask import Ui


@pytest.fixture
def app(tmpdir):
    return Flask(__name__, 
                instance_path=tmpdir.strpath, 
                instance_relative_config=True)


@pytest.fixture
def demo_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / 'fake'
    monkeypatch.syspath_prepend(str(project_dir))
    demo_dir = project_dir / 'modules/demo'
    demo_dir.mkdir(parents=True)
    contents_dir = demo_dir / 'pages/demo'
    contents_dir.mkdir(parents=True)
    return demo_dir


@pytest.fixture
def demo_name(demo_dir):
    routes_file = demo_dir / "pages/routes.py"
    routes_file.touch()
    import_name = 'modules.demo.pages.routes'
    yield import_name
    sys.modules.pop(import_name, None)


@pytest.fixture
def ui(demo_name):
    return Ui(demo_name)


def test_route_view_function(app, ui):
    @ui.route('/hello')
    def hello():
        return 'Hello World'

    app.register_blueprint(ui, url_prefix='/demo')
    client = app.test_client()
    response = client.get("/demo/hello")

    assert response.status_code == 200
    assert response.data == b'Hello World'


def test_route_class_based_view(app, ui):
    @ui.route('/hello')
    class Hello(View):
        def dispatch_request(self):
            return 'Hello World'

    app.register_blueprint(ui, url_prefix='/demo')
    client = app.test_client()
    response = client.get("/demo/hello")

    assert response.status_code == 200
    assert response.data == b'Hello World'
    
def test_route_method_view(app, ui):
    @ui.route('/hello')
    class Hello(MethodView):
        def get(self):
            return 'Hello World'

    app.register_blueprint(ui, url_prefix='/demo')
    client = app.test_client()
    response = client.get("/demo/hello")

    assert response.status_code == 200
    assert response.data == b'Hello World'