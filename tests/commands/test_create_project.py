
import os
import pytest
from click.testing import CliRunner
from pigal_flask.commands import create_project


def test_create_project_structure(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        result = runner.invoke(create_project, ['myproj'])

    project_path = os.path.join(tmpdir, 'myproj')
    assert result.exit_code == 0
    assert os.path.isdir(project_path)
    assert os.path.isdir(os.path.join(project_path, 'app'))
    assert os.path.isdir(os.path.join(project_path, 'migrations'))
    assert os.path.isdir(os.path.join(project_path, 'modules'))
    assert os.path.isdir(os.path.join(project_path, 'tests'))
    assert os.path.isdir(os.path.join(project_path, 'themes'))
    assert os.path.isdir(os.path.join(project_path, 'translations'))


def test_create_app_structure(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['myproj'])

    app_path = os.path.join(tmpdir, 'myproj', 'app')
    assert os.path.isfile(os.path.join(app_path, 'config.py'))
    assert os.path.isfile(os.path.join(app_path, 'extensions.py'))
    assert os.path.isfile(os.path.join(app_path, '__init__.py'))


def test_create_app_config_file(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['myproj'])

    file_path = os.path.join(tmpdir, 'myproj', 'app', 'config.py')
    with open(file_path, 'rt') as file:
        code = file.read()
        assert 'class Config:' in code
        assert "    PIGAL_PROJECT_NAME = 'myproj'" in code


def test_create_app_extensions_file(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['myproj'])

    file_path = os.path.join(tmpdir, 'myproj', 'app', 'extensions.py')
    with open(file_path, 'rt') as file:
        code = file.read()
        assert 'from pigal_flask import Pigal, PigalDb' in code
        assert 'db = PigalDb()' in code
        assert 'pigal = Pigal()' in code


def test_create_app_init_file(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['myproj'])

    file_path = os.path.join(tmpdir, 'myproj', 'app', '__init__.py')
    with open(file_path, 'rt') as file:
        code = file.read()
        assert 'from flask import Flask' in code
        assert 'from .extensions import db, pigal' in code
        assert 'from .config import Config' in code
        assert 'app = Flask(__name__)' in code
        assert 'app.config.from_object(Config)' in code
        assert 'pigal.init_app(app)' in code


def test_create_defaults_modules(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['myproj'])

    modules_path = os.path.join(tmpdir, 'myproj', 'modules')
    assert os.path.isdir(os.path.join(modules_path, 'home'))
    assert os.path.isdir(os.path.join(modules_path, 'auth'))
    assert os.path.isfile(os.path.join(modules_path, '__init__.py'))


def test_create_default_home_module(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['myproj'])

    home_path = os.path.join(tmpdir, 'myproj', 'modules', 'home')
    assert os.path.isdir(os.path.join(home_path, 'assets'))
    assert os.path.isdir(os.path.join(home_path, 'pages'))
    assert os.path.isfile(os.path.join(home_path, 'pages', 'index.jinja'))
    assert os.path.isfile(os.path.join(home_path, 'models.py'))
    assert os.path.isfile(os.path.join(home_path, 'ressources.py'))
    assert os.path.isfile(os.path.join(home_path, 'views.py'))
    assert os.path.isfile(os.path.join(home_path, 'services.py'))


def test_create_default_auth_module(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['myproj'])

    auth_path = os.path.join(tmpdir, 'myproj', 'modules', 'auth')
    assert os.path.isdir(os.path.join(auth_path, 'assets'))
    assert os.path.isdir(os.path.join(auth_path, 'pages'))
    assert os.path.isfile(os.path.join(auth_path, 'pages', 'login.jinja'))
    assert os.path.isfile(os.path.join(auth_path, 'models.py'))
    assert os.path.isfile(os.path.join(auth_path, 'ressources.py'))
    assert os.path.isfile(os.path.join(auth_path, 'views.py'))
    assert os.path.isfile(os.path.join(auth_path, 'services.py'))


def test_create_default_theme(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['myproj'])

    theme_path = os.path.join(tmpdir, 'myproj', 'themes', 'default')
    assert os.path.isdir(os.path.join(theme_path, 'assets'))
    assert os.path.isdir(os.path.join(theme_path, 'layouts'))
    assert os.path.isfile(os.path.join(theme_path, 'layouts', 'page.jinja'))
    assert os.path.isfile(os.path.join(theme_path, 'components.jinja'))
