
import pytest
from flask import Blueprint
from pigal_flask.utils import PigalUi


def test_is_flask_blueprint():
    assert issubclass(PigalUi, Blueprint)


@pytest.fixture
def import_file(tmpdir):
    test_dir = tmpdir / 'pages' / 'demo' / 'routes.py'
    return test_dir.strpath

def test_is_configured_with_import_file(import_file):
    static_dir = import_file.replace('routes.py', 'static')
    ui = PigalUi(import_file)
    assert ui.name == 'demo'
    assert ui.import_name == 'pages.demo.routes'
    assert ui.template_folder == 'templates'
    assert ui.static_folder == static_dir
    assert ui.static_url_path == static_dir

