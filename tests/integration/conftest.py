import os
import sys

root_dir = os.path.dirname(__file__)
while 'tests' in root_dir:
    root_dir = os.path.dirname(root_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)


import pytest
from flask import Flask

@pytest.fixture
def app(tmpdir):
    """Flask app for testing"""
    app_dir = tmpdir / 'app'
    app_dir.mkdir()
    app = Flask(__name__, 
                instance_path=app_dir, 
                instance_relative_config=True)
    app.project_dir = tmpdir
    return app

@pytest.fixture
def client(app):
    """Flask client to send http requests"""
    return app.test_client()

