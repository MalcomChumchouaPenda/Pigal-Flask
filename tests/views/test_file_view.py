
import pytest
from flask import Flask, Blueprint
from flask.views import View
from pigal_flask.views import FileView


def test_is_view():
    assert issubclass(FileView, View)

def test_accept_only_get_methods():
    assert FileView.methods == ['GET']


# @pytest.fixture
# def pages_dir(tmpdir):
#     test_dir = tmpdir / 'modules' / 'demo' / 'pages'
#     return test_dir


# def test_scan_templates(tmp_path):

#     templates = tmp_path / "templates"
#     templates.mkdir()

#     (templates / "index.html").touch()
#     (templates / "about.html").touch()

#     router = FileRouter(templates)

#     assert len(router.routes) == 2