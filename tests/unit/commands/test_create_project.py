import os
import pytest
from click.testing import CliRunner
from pigal_flask.commands import create_project


def test_create_project_structure(tmp_path, monkeypatch):
    # Given
    project_dir = tmp_path / "MyProject"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    result = runner.invoke(create_project, ["MyProject"])

    # Then
    assert result.exit_code == 0
    assert os.path.isdir(project_dir)
    assert os.path.isdir(str(project_dir / "app"))
    assert os.path.isdir(str(project_dir / "migrations"))
    assert os.path.isdir(str(project_dir / "modules"))
    assert os.path.isdir(str(project_dir / "tests"))


def test_create_app_structure(tmp_path, monkeypatch):
    # Given
    app_dir = tmp_path / "MyProject/app"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])

    # Then
    assert os.path.isdir(str(app_dir / "theme"))
    assert os.path.isfile(str(app_dir / "config.py"))
    assert os.path.isfile(str(app_dir / "extensions.py"))
    assert os.path.isfile(str(app_dir / "__init__.py"))


def test_create_app_theme(tmp_path, monkeypatch):
    # Given
    theme_dir = tmp_path / "MyProject/app/theme"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])

    # Then
    assert os.path.isdir(str(theme_dir / "static"))
    assert os.path.isdir(str(theme_dir / "templates"))


def test_create_app_theme_layouts(tmp_path, monkeypatch):
    # Given
    template_dir = tmp_path / "MyProject/app/theme/templates"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])

    # Then
    assert os.path.isfile(str(template_dir / "layouts/page.jinja"))


def test_create_app_theme_macros(tmp_path, monkeypatch):
    # Given
    template_dir = tmp_path / "MyProject/app/theme/templates"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])

    # Then
    assert os.path.isfile(str(template_dir / "macros.jinja"))


def test_create_app_config_file(tmp_path, monkeypatch):
    # Given
    file_name = tmp_path / "MyProject/app/config.py"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert 'class Config:' in code
    assert '    PIGAL_PROJECT_NAME = "MyProject"' in code
    assert '    PIGAL_PROJECT_VERSION = "0.0"' in code


def test_create_app_extensions_file(tmp_path, monkeypatch):
    # Given
    file_name = tmp_path / "MyProject/app/extensions.py"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "from pigal_flask import RouteManager" in code
    assert "route_manager = RouteManager()" in code


def test_create_app_init_file(tmp_path, monkeypatch):
    # Given
    file_name = tmp_path / "MyProject/app/__init__.py"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "from flask import Flask" in code
    assert "from .config import Config" in code
    assert "from .extensions import route_manager" in code
    assert "app = Flask(__name__)" in code
    assert "app.config.from_object(Config)" in code
    assert "route_manager.init_app(app)" in code


def test_create_default_modules(tmp_path, monkeypatch):
    # Given
    modules_dir = tmp_path / "MyProject/modules"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])

    # Then
    assert os.path.isdir(str(modules_dir / "home"))
    assert os.path.isdir(str(modules_dir / "auth"))


def test_create_home_module(tmp_path, monkeypatch):
    # Given
    home_dir = tmp_path / "MyProject/modules/home"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])

    # Then
    assert os.path.isdir(str(home_dir / "static"))
    assert os.path.isdir(str(home_dir / "templates"))
    assert os.path.isfile(str(home_dir / "config.py"))
    assert os.path.isfile(str(home_dir / "models.py"))
    assert os.path.isfile(str(home_dir / "resources.py"))
    assert os.path.isfile(str(home_dir / "services.py"))
    assert os.path.isfile(str(home_dir / "views.py"))


def test_create_home_ui(tmp_path, monkeypatch):
    # Given
    file_name = tmp_path / "MyProject/modules/home/views.py"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "from pigal_flask import ModuleUi" in code
    assert "ui = ModuleUi(__name__)" in code


def test_create_home_index_page(tmp_path, monkeypatch):
    # Given
    file_name = tmp_path / "MyProject/modules/home/templates/home/index.html"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "<h1>Welcome in <b>MyProject</b> project</h1>" in code


def test_create_auth_module(tmp_path, monkeypatch):
    # Given
    auth_dir = tmp_path / "MyProject/modules/auth"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])

    # Then
    assert os.path.isdir(str(auth_dir / "static"))
    assert os.path.isdir(str(auth_dir / "templates"))
    assert os.path.isfile(str(auth_dir / "config.py"))
    assert os.path.isfile(str(auth_dir / "models.py"))
    assert os.path.isfile(str(auth_dir / "resources.py"))
    assert os.path.isfile(str(auth_dir / "services.py"))
    assert os.path.isfile(str(auth_dir / "views.py"))


def test_create_auth_ui(tmp_path, monkeypatch):
    # Given
    file_name = tmp_path / "MyProject/modules/auth/views.py"
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    runner.invoke(create_project, ["MyProject"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "from pigal_flask import ModuleUi" in code
    assert "ui = ModuleUi(__name__)" in code
