
import sys
import importlib
import pytest


extensions_code = """
from pigal_flask import Pigal, PigalDb

db = PigalDb()
pigal = Pigal()
"""

config_code = """
class Config:
    PIGAL_PROJECT_NAME = 'demo'
    PIGAL_PROJECT_VERSION = '0.1'
    PIGAL_DB_URI_TEMPLATE = 'sqlite:///{project_dir}/databases/{service_id}.db'
"""

app_code = """
from flask import Flask
from .extensions import db, pigal
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
pigal.init_app(app)
"""

models_code = """
from app.extensions import db

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
"""


@pytest.fixture
def db_project1(tmpdir):
    """Flask app with and services"""
    # make project app structure
    project_dir = tmpdir
    app_dir = project_dir / 'app'
    app_dir.mkdir()
    app = app_dir / '__init__.py'
    app.write_text(app_code, encoding='utf-8')
    config = app_dir / 'config.py'
    config.write_text(config_code, encoding='utf-8')
    extensions = app_dir / 'extensions.py'
    extensions.write_text(extensions_code, encoding='utf-8')

    # make project plugin directories
    databases_dir = project_dir / 'databases'
    databases_dir.mkdir()
    services_dir = project_dir / 'services'
    services_dir.mkdir()
    pages_dir = project_dir / 'pages'
    pages_dir.mkdir()

    # create models inside services
    for name in ('demo_v1', 'demo_v2'):
        service_dir = services_dir / name
        service_dir.mkdir()
        routes = service_dir / 'models.py'
        routes.write_text(models_code, encoding='utf-8')
        
    # include in PYTHONPATH
    project_path = project_dir.strpath
    if project_path not in sys.path:
        sys.path.append(project_path)
    
    # import module app and db
    module = importlib.import_module('app')
    return module.app, module.db


@pytest.mark.parametrize('service_id', ['demo_v1', 'demo_v2'])
def test_create_all_table(db_project1, service_id):
    app, db = db_project1
    with app.app_context():
        db.drop_all()
        db.create_all()

        models_dir = f'services.{service_id}.models'
        models = importlib.import_module(models_dir)
        person1 = models.Person(id=1, name='Demo A')
        person2 = models.Person(id=2, name='Demo B')
        db.session.add_all([person1, person2])
        db.session.commit()
        assert db.session.query(models.Person).count() == 2

        