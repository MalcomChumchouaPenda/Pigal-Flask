
import pytest
from flask_restx import Namespace, Model, fields
from pigal_flask.utils import PigalApi


def test_is_flask_rest_namespace():
    assert issubclass(PigalApi, Namespace)


@pytest.fixture
def import_file(tmpdir):
    test_dir = tmpdir / 'services' / 'demo_v0' / 'routes.py'
    return test_dir.strpath

def test_is_configured_by_import_file(import_file):
    api = PigalApi(import_file)
    assert api.name == 'demo_v0'
    assert api.path == '/demo/v0'

def test_add_prefix_to_api_model(import_file):
    api = PigalApi(import_file)
    model = api.model('Any', {'id':fields.String()})
    assert isinstance(model, Model)
    assert model.name == 'demo_v0.Any'
    
