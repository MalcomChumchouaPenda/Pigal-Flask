
import pytest
from flask import Blueprint
from pigal_flask.routers import WebUi


def test_is_flask_blueprint():
    assert issubclass(WebUi, Blueprint)


@pytest.fixture
def import_file(tmpdir):
    test_dir = tmpdir / 'modules' / 'demo' / 'routers.py'
    return test_dir.strpath

def test_is_configured_with_import_file(import_file):
    ui = WebUi(import_file)
    assert ui.name == 'demo'
    assert ui.import_name == 'modules.demo.routers'
    assert ui.template_folder == 'pages'
    assert ui.static_folder == import_file.replace('routers.py', 'assets')
    assert ui.static_url_path == import_file.replace('routers.py', 'assets')

