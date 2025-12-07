
import os
import sys

tests_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(tests_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)


import tempfile
import pytest
from flask import Flask


@pytest.fixture
def app():
    """Flask app for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        app_dir = os.path.join(temp_dir, 'app')
        app = Flask(__name__, 
                    instance_path=app_dir, 
                    instance_relative_config=True)
        yield app

@pytest.fixture
def client(app):
    """Flask client to send http requests"""
    return app.test_client()

