
import os
import pytest
from click.testing import CliRunner
from pigal_flask.commands import create_project


def test_create_project_structure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(create_project, ['myproject'])

    project_dir = tmp_path / 'myproject'
    assert result.exit_code == 0
    assert os.path.isdir(project_dir)
    assert os.path.isdir(str(project_dir / 'app'))
    assert os.path.isdir(str(project_dir / 'migrations'))
    assert os.path.isdir(str(project_dir / 'modules'))
    assert os.path.isdir(str(project_dir / 'tests'))
    assert os.path.isdir(str(project_dir / 'themes'))
    assert os.path.isdir(str(project_dir / 'translations'))


def test_create_app_structure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    app_dir = tmp_path / 'myproject/app'
    assert os.path.isfile(str(app_dir / 'config.py'))
    assert os.path.isfile(str(app_dir / 'extensions.py'))
    assert os.path.isfile(str(app_dir / '__init__.py'))


def test_create_app_config_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    file_name = tmp_path / 'myproject/app/config.py'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert 'class Config:' in code
        assert "    PIGAL_PROJECT_NAME = 'myproject'" in code
        assert "    PIGAL_PROJECT_VERSION = '0.0'" in code


def test_create_app_extensions_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    file_name = tmp_path / 'myproject/app/extensions.py'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert 'from pigal_flask import RouteManager' in code
        assert 'route_manager = RouteManager()' in code


def test_create_app_init_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    file_name = tmp_path / 'myproject/app/__init__.py'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert 'from flask import Flask' in code
        assert 'from .config import Config' in code
        assert 'from .extensions import route_manager' in code
        assert 'app = Flask(__name__)' in code
        assert 'app.config.from_object(Config)' in code
        assert 'route_manager.init_app(app)' in code


def test_create_default_modules(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    modules_dir = tmp_path / 'myproject/modules'
    assert os.path.isdir(str(modules_dir / 'home'))
    assert os.path.isdir(str(modules_dir / 'auth'))


def test_create_home_module(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    home_dir = tmp_path / 'myproject/modules/home'
    assert os.path.isdir(str(home_dir / 'pages'))
    assert os.path.isdir(str(home_dir / 'services'))
    assert os.path.isdir(str(home_dir / 'static'))
    

def test_create_home_pages(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    home_dir = tmp_path / 'myproject/modules/home'
    assert os.path.isfile(str(home_dir / 'pages/home/index.html'))
    assert os.path.isfile(str(home_dir / 'pages/routes.py'))

    
def test_create_home_pages_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    home_dir = tmp_path / 'myproject/modules/home'
    file_name = home_dir / 'pages/routes.py'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert 'from pigal_flask import ModuleUi' in code
        assert 'ui = ModuleUi(__name__)' in code


def test_create_home_pages_index(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    home_dir = tmp_path / 'myproject/modules/home'
    file_name = home_dir / 'pages/home/index.html'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert '<h1>Welcome in <b>myproject</b> project</h1>' in code


def test_create_auth_module(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    auth_dir = tmp_path / 'myproject/modules/auth'
    assert os.path.isdir(str(auth_dir / 'pages'))
    assert os.path.isdir(str(auth_dir / 'services'))
    assert os.path.isdir(str(auth_dir / 'static'))


def test_create_auth_pages(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    auth_dir = tmp_path / 'myproject/modules/auth'
    assert os.path.isfile(str(auth_dir / 'pages/auth/login.html'))
    assert os.path.isfile(str(auth_dir / 'pages/routes.py'))

    
def test_create_auth_pages_routes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    home_dir = tmp_path / 'myproject/modules/auth'
    file_name = home_dir / 'pages/routes.py'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert 'from pigal_flask import ModuleUi' in code
        assert 'ui = ModuleUi(__name__)' in code


def test_create_default_theme(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(create_project, ['myproject'])

    theme_dir = tmp_path / 'myproject/themes/default'
    assert os.path.isdir(str(theme_dir / 'static'))
    assert os.path.isdir(str(theme_dir / 'layouts'))
    assert os.path.isfile(str(theme_dir / 'layouts/page.jinja'))
    assert os.path.isfile(str(theme_dir / 'macros.jinja'))
