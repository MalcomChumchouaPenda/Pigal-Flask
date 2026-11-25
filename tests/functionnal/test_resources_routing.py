import os
import sys
import pytest
from flask import Flask
from pigal_flask.extensions import ProjectManager


@pytest.fixture
def project_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / "myproj"
    (project_dir / "app").mkdir(parents=True)
    (project_dir / "modules").mkdir(parents=True)
    monkeypatch.syspath_prepend(str(project_dir))
    return project_dir


@pytest.fixture
def app(project_dir):
    app = Flask(
        __name__, instance_path=str(project_dir / "app"), instance_relative_config=True
    )
    app.config["PIGAL_PROJECT_NAME"] = "myproj"
    app.config["PIGAL_PROJECT_VERSION"] = "1.0"
    return app


def test_route_default_api_doc(app):
    project_manager = ProjectManager()
    project_manager.init_app(app)

    with app.test_client() as client:
        response = client.get("/api/")
        assert response.status_code == 200
        assert "myproj API" in response.data.decode()
        assert "swagger" in response.data.decode()


REST_CODE = """
    \nfrom flask_restx import Resource, Api
    \nfrom pigal_flask import RestApi

    \nrest_api = RestApi(__name__)

    \n@rest_api.route('/hello')
    \nclass HelloWorld(Resource):
    \n    def get(self):
    \n        return {'message': 'Hello, World!'}
    """


def test_route_minimal_rest_api(app, project_dir):
    module_dir = project_dir / "modules/demo"
    module_dir.mkdir(parents=True)
    service_file = module_dir / "resources.py"
    service_file.write_text(REST_CODE, encoding="utf-8")
    project_manager = ProjectManager()
    project_manager.init_app(app)

    with app.test_client() as client:
        response = client.get("/api/demo/v0/hello")
        assert response.status_code == 200
        assert response.json == {"message": "Hello, World!"}
