import os
import pytest
from click.testing import CliRunner
from pigal_flask.commands import create_project


@pytest.fixture
def project_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / "MyProject"
    monkeypatch.chdir(tmp_path)
    return project_dir


def test_create_project_structure(project_dir):
    # Given
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


def test_create_app_structure(project_dir):
    # Given
    runner = CliRunner()
    app_dir = project_dir / "app"

    # When
    runner.invoke(create_project, ["MyProject"])

    # Then
    assert os.path.isdir(str(app_dir / "theme"))
    assert os.path.isfile(str(app_dir / "config.py"))
    assert os.path.isfile(str(app_dir / "extensions.py"))
    assert os.path.isfile(str(app_dir / "__init__.py"))


def test_create_app_theme(project_dir):
    # Given
    runner = CliRunner()
    theme_dir = project_dir / "app/theme"

    # When
    runner.invoke(create_project, ["MyProject"])

    # Then
    assert os.path.isdir(str(theme_dir / "static"))
    assert os.path.isdir(str(theme_dir / "templates"))


def test_create_app_theme_layouts(project_dir):
    # Given
    runner = CliRunner()
    template_dir = project_dir / "app/theme/templates"

    # When
    runner.invoke(create_project, ["MyProject"])

    # Then
    assert os.path.isfile(str(template_dir / "layouts/page.jinja"))


def test_create_app_theme_macros(project_dir):
    # Given
    runner = CliRunner()
    template_dir = project_dir / "app/theme/templates"

    # When
    runner.invoke(create_project, ["MyProject"])

    # Then
    assert os.path.isfile(str(template_dir / "macros.jinja"))


def test_create_app_config_file(project_dir):
    # Given
    runner = CliRunner()
    file_name = project_dir / "app/config.py"

    # When
    runner.invoke(create_project, ["MyProject"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "class Config:" in code
    assert '    PIGAL_PROJECT_NAME = "MyProject"' in code
    assert '    PIGAL_PROJECT_VERSION = "0.0"' in code


def test_create_app_extensions_file(project_dir):
    # Given
    runner = CliRunner()
    file_name = project_dir / "app/extensions.py"

    # When
    runner.invoke(create_project, ["MyProject"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "from pigal_flask import ProjectManager" in code
    assert "project_manager = ProjectManager()" in code


def test_create_app_init_file(project_dir):
    # Given
    runner = CliRunner()
    file_name = project_dir / "app/__init__.py"

    # When
    runner.invoke(create_project, ["MyProject"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "from flask import Flask" in code
    assert "from .config import Config" in code
    assert "from .extensions import project_manager" in code
    assert "app = Flask(__name__)" in code
    assert "app.config.from_object(Config)" in code
    assert "project_manager.init_app(app)" in code


def test_create_default_modules(project_dir):
    # Given
    runner = CliRunner()
    modules_dir = project_dir / "modules"

    # When
    runner.invoke(create_project, ["MyProject"])

    # Then
    assert os.path.isdir(str(modules_dir / "home"))
    assert os.path.isdir(str(modules_dir / "auth"))


def test_create_home_module(project_dir):
    # Given
    runner = CliRunner()
    home_dir = project_dir / "modules/home"

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


def test_create_home_ui(project_dir):
    # Given
    runner = CliRunner()
    file_name = project_dir / "modules/home/views.py"

    # When
    runner.invoke(create_project, ["MyProject"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "from pigal_flask import Ui" in code
    assert "ui = Ui(__name__)" in code


def test_create_home_index_page(project_dir):
    # Given
    runner = CliRunner()
    file_name = project_dir / "modules/home/templates/home/index.html"

    # When
    runner.invoke(create_project, ["MyProject"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "<h1>Welcome in <b>MyProject</b> project</h1>" in code


def test_create_auth_module(project_dir):
    # Given
    runner = CliRunner()
    auth_dir = project_dir / "modules/auth"

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


def test_create_auth_ui(project_dir):
    # Given
    runner = CliRunner()
    file_name = project_dir / "modules/auth/views.py"

    # When
    runner.invoke(create_project, ["MyProject"])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "from pigal_flask import Ui" in code
    assert "ui = Ui(__name__)" in code
