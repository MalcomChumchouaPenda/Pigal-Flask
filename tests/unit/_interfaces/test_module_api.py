
import os
import sys
import pytest
from unittest.mock import MagicMock
from flask_restx import Namespace
import pigal_flask._interfaces as pkg


def test_is_flask_rest_namespace():
    assert issubclass(pkg.ModuleApi, Namespace)


@pytest.fixture
def services_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / 'fake'
    monkeypatch.syspath_prepend(str(project_dir))
    services_dir = project_dir / 'modules/demo/services'
    services_dir.mkdir(parents=True)
    return services_dir


@pytest.fixture
def import_name(services_dir):
    views_file = services_dir / "demo_v1.py"
    views_file.touch()
    import_name = 'modules.demo.pages.demo_v1'
    yield import_name
    sys.modules.pop(import_name, None)


def test_is_configured_with_import_name(import_name):
    api = pkg.ModuleApi(import_name)
    assert api.import_name == import_name


def test_has_generated_name(import_name):
    api = pkg.ModuleApi(import_name)
    assert api.name == 'demo_v1'


def test_has_generated_descr(import_name):
    api = pkg.ModuleApi(import_name)
    assert api.description == 'demo_v1 service'
    

def test_model_by_adding_specific_prefix(import_name):
    api = pkg.ModuleApi(import_name)
    model = api.model('Any', {})
    assert model.name == 'demo_v1.Any'
    
