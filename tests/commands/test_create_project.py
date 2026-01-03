
import os
import pytest
import zipfile as zpf
from click.testing import CliRunner
from pigal_flask.commands import create_project


@pytest.fixture
def fake_theme(tmpdir):
    test_file = tmpdir / 'hi.txt'
    test_file.write('fake text for test')
    theme_zip = tmpdir / 'fake_theme_0.zip'
    with zpf.ZipFile(theme_zip, 'w') as file:
        for name in ('static', 'templates'):
            file.write(test_file, arcname=f'{name}/hi.txt')
    return theme_zip.strpath


def test_create_project_structure(tmpdir, change_dir, fake_theme):
    runner = CliRunner()
    with change_dir(tmpdir):
        result = runner.invoke(create_project, ['test', fake_theme])

    project_path = os.path.join(tmpdir, 'test')
    assert result.exit_code == 0
    assert os.path.isdir(project_path)
    assert os.path.isdir(os.path.join(project_path, 'app'))
    assert os.path.isdir(os.path.join(project_path, 'pages'))
    assert os.path.isdir(os.path.join(project_path, 'services'))


def test_unzip_theme_in_project(tmpdir, change_dir, fake_theme):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['test', fake_theme])

    app_path = os.path.join(tmpdir, 'test', 'app')
    for name in ('static', 'templates'):
        assert os.path.isdir(os.path.join(app_path, name))
        assert os.path.isfile(os.path.join(app_path, name, 'hi.txt'))
    

def test_create_app_structure(tmpdir, change_dir, fake_theme):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['test', fake_theme])

    app_path = os.path.join(tmpdir, 'test', 'app')
    assert os.path.isfile(os.path.join(app_path, 'config.py'))
    assert os.path.isfile(os.path.join(app_path, 'extensions.py'))
    assert os.path.isfile(os.path.join(app_path, '__init__.py'))


def test_create_app_config_file(tmpdir, change_dir, fake_theme):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['test', fake_theme])

    file_path = os.path.join(tmpdir, 'test', 'app', 'config.py')
    with open(file_path, 'rt') as file:
        code = file.read()
        assert 'class Config:' in code
        assert "    PIGAL_PROJECT_NAME = 'test'" in code


def test_create_app_extensions_file(tmpdir, change_dir, fake_theme):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['test', fake_theme])

    file_path = os.path.join(tmpdir, 'test', 'app', 'extensions.py')
    with open(file_path, 'rt') as file:
        code = file.read()
        assert 'from pigal_flask import Pigal, PigalDb' in code
        assert 'db = PigalDb()' in code
        assert 'pigal = Pigal()' in code


def test_create_app_init_file(tmpdir, change_dir, fake_theme):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['test', fake_theme])

    file_path = os.path.join(tmpdir, 'test', 'app', '__init__.py')
    with open(file_path, 'rt') as file:
        code = file.read()
        assert 'from flask import Flask' in code
        assert 'from .extensions import db, pigal' in code
        assert 'from .config import Config' in code
        assert 'app = Flask(__name__)' in code
        assert 'app.config.from_object(Config)' in code
        assert 'pigal.init_app(app)' in code


def test_create_pages_structure(tmpdir, change_dir, fake_theme):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['test', fake_theme])

    pages_path = os.path.join(tmpdir, 'test', 'pages')
    assert os.path.isdir(os.path.join(pages_path, 'home'))
    assert os.path.isfile(os.path.join(pages_path, '__init__.py'))


def test_create_default_home_page(tmpdir, change_dir, fake_theme):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['test', fake_theme])

    home_path = os.path.join(tmpdir, 'test', 'pages', 'home')
    assert os.path.isdir(os.path.join(home_path, 'static'))
    assert os.path.isdir(os.path.join(home_path, 'templates'))
    assert os.path.isdir(os.path.join(home_path, 'templates', 'home'))
    assert os.path.isfile(os.path.join(home_path, 'forms.py'))
    assert os.path.isfile(os.path.join(home_path, 'routes.py'))


def test_create_services_structure(tmpdir, change_dir, fake_theme):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['test', fake_theme])

    services_path = os.path.join(tmpdir, 'test', 'services')
    assert os.path.isdir(os.path.join(services_path, 'auth'))
    assert os.path.isfile(os.path.join(services_path, '__init__.py'))


def test_create_default_auth_service(tmpdir, change_dir, fake_theme):
    runner = CliRunner()
    with change_dir(tmpdir):
        runner.invoke(create_project, ['test', fake_theme])

    auth_path = os.path.join(tmpdir, 'test', 'services', 'auth')
    assert os.path.isdir(os.path.join(auth_path, 'store'))
    assert os.path.isfile(os.path.join(auth_path, 'utils.py'))
    assert os.path.isfile(os.path.join(auth_path, 'models.py'))
    assert os.path.isfile(os.path.join(auth_path, 'routes.py'))

