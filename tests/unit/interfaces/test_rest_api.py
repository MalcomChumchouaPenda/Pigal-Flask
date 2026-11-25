import os
import sys
import pytest
from unittest.mock import MagicMock
from flask_restx import Namespace
import pigal_flask.interfaces as pkg


def test_is_flask_rest_namespace():
    assert issubclass(pkg.RestApi, Namespace)


@pytest.fixture
def module_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / "fake"
    monkeypatch.syspath_prepend(str(project_dir))
    module_dir = project_dir / "modules/demo"
    module_dir.mkdir(parents=True)
    return module_dir


@pytest.fixture
def import_name(module_dir):
    views_file = module_dir / "resources.py"
    views_file.touch()
    import_name = "modules.demo.resources"
    yield import_name
    sys.modules.pop(import_name, None)


def test_is_configured_with_import_name(import_name):
    api = pkg.RestApi(import_name)
    assert api.import_name == import_name


def test_has_generated_name(import_name):
    api = pkg.RestApi(import_name)
    assert api.name == "demo_v0"


def test_has_generated_descr(import_name):
    api = pkg.RestApi(import_name)
    assert api.description == "demo_v0 Rest-Full API"


def test_model_by_adding_specific_prefix(import_name):
    api = pkg.RestApi(import_name)
    model = api.model("Any", {})
    assert model.name == "demo_v0.Any"
