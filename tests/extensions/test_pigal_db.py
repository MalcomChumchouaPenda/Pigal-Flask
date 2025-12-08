
import os
import sys
import importlib
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pigal_flask.extensions import PigalDb, InvalidProjectConfig


def test_is_sqlachemy_instance():
    assert issubclass(PigalDb, SQLAlchemy)


@pytest.fixture
def app1(tmpdir):
    """Flask app without db config"""
    project_path = tmpdir.strpath
    if project_path not in sys.path:
        sys.path.append(project_path)
    services_dir = tmpdir / 'services'
    services_dir.mkdir()
    app_dir = tmpdir / 'app'
    app_dir.mkdir()
    app = Flask(__name__, 
                instance_path=app_dir, 
                instance_relative_config=True)
    app.services_dir = services_dir
    app.project_dir = tmpdir
    return app

def test_requires_project_name_in_app_config(app1):
    app = app1
    with pytest.raises(InvalidProjectConfig) as exc_info:
        db = PigalDb()
        db.init_app(app)
    err_msg = "Configuration parameter 'PIGAL_DB_URI_TEMPLATE' is missing"
    assert str(exc_info.value) == err_msg


@pytest.mark.parametrize('uri_template', [
    'sqlite:///{project_dir}/{service_id}.db',
    'sqlite:///{project_dir}/test_{service_id}.db',
    'sqlite:///{project_dir}/{service_id}_test.db',
    ])
def test_creates_default_sqlalchemy_uri(app1, uri_template):
    app1.config['PIGAL_DB_URI_TEMPLATE'] = uri_template
    app = app1
    db = PigalDb()
    db.init_app(app)
    project_path = app.project_dir.strpath
    kwargs = {'service_id': 'default', 'project_dir':project_path}
    assert uri_template.format_map(kwargs) == app.config['SQLALCHEMY_DATABASE_URI']


@pytest.fixture
def app2(app1):
    """Flask app with services models"""    
    app = app1
    services_dir = app.services_dir
    for name in ('demo_v1', 'demo_v2'):
        service_dir = services_dir / name
        service_dir.mkdir()
        models = service_dir / 'models.py'
        models.write_text('', encoding='utf-8')
    return app


@pytest.mark.parametrize('uri_template', [
    'sqlite:///{project_dir}/{service_id}.db',
    'sqlite:///{project_dir}/test_{service_id}.db',
    'sqlite:///{project_dir}/{service_id}_test.db',
    ])
def test_creates_sqlalchemy_binds_by_service(app2, uri_template):
    app2.config['PIGAL_DB_URI_TEMPLATE'] = uri_template
    app = app2
    db = PigalDb()
    db.init_app(app)
    db_binds = app.config['SQLALCHEMY_BINDS']
    project_path = app.project_dir.strpath
    for name in ('demo_v1', 'demo_v2'):
        kwargs = {'service_id': name, 'project_dir':project_path}
        assert uri_template.format_map(kwargs) == db_binds[name]


@pytest.fixture
def app3(app1):
    """Flask app with private services directories"""    
    app = app1
    services_dir = app.services_dir
    for name in ('_demo_v1', '__demo_v2'):
        service_dir = services_dir / name
        service_dir.mkdir()
        models = service_dir / 'models.py'
        models.write_text('', encoding='utf-8')
    return app

def test_ignores_private_directories_in_services_directory(app3):
    app3.config['PIGAL_DB_URI_TEMPLATE'] = 'sqlite:///{service_id}.db'
    app = app3
    db = PigalDb()
    db.init_app(app)
    assert len(app.config['SQLALCHEMY_BINDS']) == 0


@pytest.fixture
def db1(app1):
    """Flask app with default db uri template"""    
    app = app1
    app.config['PIGAL_DB_URI_TEMPLATE'] = 'sqlite:///{service_id}.db'
    db = PigalDb(app)
    return db

def test_provides_model_class_which_generated_attrs(db1):
    class Person(db1.Model):
        __module__ = 'services.demo_v0.models'
        id = db1.Column(db1.Integer, primary_key=True)
    assert Person.__tablename__ == 'demo_v0_person'
    assert Person.__bind_key__ == 'demo_v0'

