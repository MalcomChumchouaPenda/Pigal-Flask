
import pytest
from flask_restx import Namespace
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
