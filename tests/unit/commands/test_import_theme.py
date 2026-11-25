import os
import zipfile
import pytest
from click.testing import CliRunner
from pigal_flask.commands import import_theme


@pytest.fixture
def project_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / "fakeproject"
    (project_dir / "app/theme/static").mkdir(parents=True)
    (project_dir / "app/theme/templates/layouts").mkdir(parents=True)
    monkeypatch.chdir(project_dir)
    return project_dir


@pytest.fixture
def theme_dir(project_dir):
    theme_dir = project_dir / "app/theme"
    templates_dir = theme_dir / "templates"
    (theme_dir / "static/style.css").write_text("body {}", encoding="utf-8")
    (templates_dir / "layouts/base.jinja").write_text(
        "<html>old</html>", encoding="utf-8"
    )
    (templates_dir / "macros.jinja").write_text(
        "{% macro test1() %}{% endmacro %}", encoding="utf-8"
    )
    return theme_dir


@pytest.fixture
def new_theme_zip(tmp_path):
    zip_path = tmp_path / "new_theme.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        archive.writestr("static/style2.css", "body {}")
        archive.writestr("templates/layouts/base.jinja", "<html>new</html>")
        archive.writestr("templates/macros.jinja", "{% macro test2() %}{% endmacro %}")
    return zip_path


def test_replace_theme_static(theme_dir, new_theme_zip):
    # Given
    runner = CliRunner()

    # When
    runner.invoke(import_theme, [str(new_theme_zip)])

    # Then
    assert os.path.isfile(theme_dir / "static/style2.css")
    assert not os.path.isfile(theme_dir / "static/style.css")


def test_replace_theme_base_layout(theme_dir, new_theme_zip):
    # Given
    runner = CliRunner()
    file_name = theme_dir / "templates/layouts/base.jinja"

    # When
    runner.invoke(import_theme, [str(new_theme_zip)])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "<html>new</html>" in code


def test_replace_theme_macros(theme_dir, new_theme_zip):
    # Given
    runner = CliRunner()
    file_name = theme_dir / "templates/macros.jinja"

    # When
    runner.invoke(import_theme, [str(new_theme_zip)])
    with open(file_name, "rt") as file:
        code = file.read()

    # Then
    assert "{% macro test2() %}{% endmacro %}" in code


def test_fails_outside_project_dir(tmp_path, new_theme_zip, monkeypatch):
    # Given
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    # When
    result = runner.invoke(import_theme, [str(new_theme_zip)])

    # Then
    assert result.exit_code != 0
    assert "import-theme must be executed from a project dir" in result.output
