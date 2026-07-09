
import os
import pytest
from click.testing import CliRunner
from pigal_flask.commands import create_project


def test_create_project_structure(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        result = runner.invoke(create_project, ['myproj'])

    project_dir = tmp_path / 'myproj'
    assert result.exit_code == 0
    assert os.path.isdir(project_dir)
    assert os.path.isdir(str(project_dir / 'app'))
    assert os.path.isdir(str(project_dir / 'migrations'))
    assert os.path.isdir(str(project_dir / 'modules'))
    assert os.path.isdir(str(project_dir / 'tests'))
    assert os.path.isdir(str(project_dir / 'themes'))
    assert os.path.isdir(str(project_dir / 'translations'))


def test_create_app_structure(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        runner.invoke(create_project, ['myproj'])

    app_dir = tmp_path / 'myproj/app'
    assert os.path.isfile(str(app_dir / 'config.py'))
    assert os.path.isfile(str(app_dir / 'extensions.py'))
    assert os.path.isfile(str(app_dir / '__init__.py'))


def test_create_app_config_file(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        runner.invoke(create_project, ['myproj'])

    file_name = tmp_path / 'myproj/app/config.py'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert 'class Config:' in code
        assert "    PIGAL_PROJECT_NAME = 'myproj'" in code
        assert "    PIGAL_PROJECT_VERSION = '0.0'" in code


def test_create_app_extensions_file(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        runner.invoke(create_project, ['myproj'])

    file_name = tmp_path / 'myproj/app/extensions.py'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert 'from pigal_flask import Pigal' in code
        assert 'pigal = Pigal()' in code


def test_create_app_init_file(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        runner.invoke(create_project, ['myproj'])

    file_name = tmp_path / 'myproj/app/__init__.py'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert 'from flask import Flask' in code
        assert 'from .extensions import pigal' in code
        assert 'from .config import Config' in code
        assert 'app = Flask(__name__)' in code
        assert 'app.config.from_object(Config)' in code
        assert 'pigal.init_app(app)' in code


def test_create_defaults_modules(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        runner.invoke(create_project, ['myproj'])

    modules_dir = tmp_path / 'myproj/modules'
    assert os.path.isdir(str(modules_dir / 'home'))
    assert os.path.isdir(str(modules_dir / 'auth'))


def test_create_home_module(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        runner.invoke(create_project, ['myproj'])

    home_dir = tmp_path / 'myproj/modules/home'
    assert os.path.isdir(str(home_dir / 'static'))
    assert os.path.isdir(str(home_dir / 'pages'))
    assert os.path.isfile(str(home_dir / 'pages/index.html'))
    assert os.path.isfile(str(home_dir / 'models.py'))
    assert os.path.isfile(str(home_dir / 'resources.py'))
    assert os.path.isfile(str(home_dir / 'services.py'))
    assert os.path.isfile(str(home_dir / 'views.py'))


def test_create_home_module(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        runner.invoke(create_project, ['myproj'])

    home_dir = tmp_path / 'myproj/modules/home'
    assert os.path.isdir(str(home_dir / 'pages'))
    assert os.path.isdir(str(home_dir / 'static'))
    assert os.path.isfile(str(home_dir / 'models.py'))
    assert os.path.isfile(str(home_dir / 'resources.py'))
    assert os.path.isfile(str(home_dir / 'services.py'))
    assert os.path.isfile(str(home_dir / 'views.py'))

    
def test_create_home_views_file(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        runner.invoke(create_project, ['myproj'])

    home_dir = tmp_path / 'myproj/modules/home'
    file_name = home_dir / 'views.py'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert 'from pigal_flask import ModuleUi' in code
        assert 'ui = ModuleUi(__name__)' in code


def test_create_home_index_file(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        runner.invoke(create_project, ['myproj'])

    home_dir = tmp_path / 'myproj/modules/home'
    file_name = home_dir / 'pages/index.html'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert '<h1>Welcome in <b>myproj</b> project</h1>' in code


def test_create_auth_module(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        runner.invoke(create_project, ['myproj'])

    auth_dir = tmp_path / 'myproj/modules/auth'
    assert os.path.isdir(str(auth_dir / 'pages'))
    assert os.path.isdir(str(auth_dir / 'static'))
    assert os.path.isfile(str(auth_dir / 'models.py'))
    assert os.path.isfile(str(auth_dir / 'resources.py'))
    assert os.path.isfile(str(auth_dir / 'services.py'))
    assert os.path.isfile(str(auth_dir / 'views.py'))

    
def test_create_auth_views_file(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        runner.invoke(create_project, ['myproj'])

    home_dir = tmp_path / 'myproj/modules/auth'
    file_name = home_dir / 'views.py'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert 'from pigal_flask import ModuleUi' in code
        assert 'ui = ModuleUi(__name__)' in code


def test_create_default_theme(tmp_path, change_dir):
    runner = CliRunner()
    with change_dir(tmp_path):
        runner.invoke(create_project, ['myproj'])

    theme_dir = tmp_path / 'myproj/themes/default'
    assert os.path.isdir(str(theme_dir / 'static'))
    assert os.path.isdir(str(theme_dir / 'layouts'))
    assert os.path.isfile(str(theme_dir / 'layouts/page.jinja'))
    assert os.path.isfile(str(theme_dir / 'components.jinja'))
