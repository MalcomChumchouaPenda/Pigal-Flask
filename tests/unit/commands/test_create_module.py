
import os
import pytest
from click.testing import CliRunner
from pigal_flask.commands import create_module


@pytest.fixture
def project_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / 'fakeproject'
    (project_dir / 'app').mkdir(parents=True)
    (project_dir / 'modules').mkdir()
    monkeypatch.chdir(project_dir)
    return project_dir


def test_create_module_structure(project_dir):
    runner = CliRunner()
    result = runner.invoke(create_module, ['mymodule'])

    module_dir = project_dir / 'mymodule'
    assert result.exit_code == 0
    assert os.path.isdir(module_dir)
    assert os.path.isdir(str(module_dir / 'pages'))
    assert os.path.isdir(str(module_dir / 'services'))
    assert os.path.isdir(str(module_dir / 'static'))


def test_create_pages_structure(project_dir):
    runner = CliRunner()
    runner.invoke(create_module, ['mymodule'])

    pages_dir = project_dir / 'mymodule/pages'
    assert os.path.isdir(str(pages_dir / 'mymodule'))
    assert os.path.isfile(str(pages_dir / 'routes.py'))


def test_create_pages_routes_file(project_dir):
    runner = CliRunner()
    runner.invoke(create_module, ['mymodule'])

    file_name = project_dir / 'mymodule/pages/routes.py'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert 'from pigal_flask import ModuleUi' in code
        assert "ui = ModuleUi(__name__)" in code


def test_create_first_default_services(project_dir):
    runner = CliRunner()
    runner.invoke(create_module, ['mymodule'])

    file_name = project_dir / 'mymodule/services/mymodule_v1.py'
    with open(file_name, 'rt') as file:
        code = file.read()
        assert 'from pigal_flask import ModuleApi' in code
        assert "api = ModuleApi(__name__)" in code


def test_fails_outside_project_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(create_module, ['mymodule'])

    assert result.exit_code != 0
    assert "create-module must be executed from project dir" in result.output
