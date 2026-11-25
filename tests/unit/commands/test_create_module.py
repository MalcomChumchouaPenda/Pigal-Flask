import os
import pytest
from click.testing import CliRunner
from pigal_flask.commands import create_module


@pytest.fixture
def project_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / "fakeproject"
    (project_dir / "app").mkdir(parents=True)
    (project_dir / "modules").mkdir()
    monkeypatch.chdir(project_dir)
    return project_dir


def test_create_module_structure(project_dir):
    # Given
    module_dir = project_dir / "my_module"
    runner = CliRunner()

    # When
    result = runner.invoke(create_module, ["my_module"])

    # Then
    assert result.exit_code == 0
    assert os.path.isdir(str(module_dir / "static"))
    assert os.path.isdir(str(module_dir / "templates/my_module"))
    assert os.path.isfile(str(module_dir / "config.py"))
    assert os.path.isfile(str(module_dir / "models.py"))
    assert os.path.isfile(str(module_dir / "resources.py"))
    assert os.path.isfile(str(module_dir / "services.py"))
    assert os.path.isfile(str(module_dir / "views.py"))


def test_create_module_ui(project_dir):
    # Given
    file_name = project_dir / "my_module/views.py"
    runner = CliRunner()

    # When
    runner.invoke(create_module, ["my_module"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "from pigal_flask import Ui" in code
    assert "ui = Ui(__name__)" in code


def test_create_module_public_api(project_dir):
    # Given
    runner = CliRunner()
    file_name = project_dir / "my_module/services.py"

    # When
    runner.invoke(create_module, ["my_module"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "from pigal_flask import PublicApi" in code
    assert "api = PublicApi(__name__)" in code


def test_fails_outside_project_dir(tmp_path, monkeypatch):
    # Given
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    result = runner.invoke(create_module, ["my_module"])

    # Then
    assert result.exit_code != 0
    assert "create-module must be executed from project dir" in result.output
