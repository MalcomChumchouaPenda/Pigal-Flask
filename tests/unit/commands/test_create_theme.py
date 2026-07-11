
import os
import pytest
from click.testing import CliRunner
from pigal_flask.commands import create_theme


@pytest.fixture
def project_dir(tmp_path, monkeypatch):
    project_dir = tmp_path / 'fakeproject'
    (project_dir / 'app').mkdir(parents=True)
    (project_dir / 'themes').mkdir()
    monkeypatch.chdir(project_dir)
    return project_dir


def test_create_theme_structure(project_dir):
    runner = CliRunner()
    result = runner.invoke(create_theme, ['mytheme'])

    theme_dir = project_dir / 'mytheme'
    assert result.exit_code == 0
    assert os.path.isdir(theme_dir)
    assert os.path.isdir(str(theme_dir / 'layouts'))
    assert os.path.isdir(str(theme_dir / 'static'))
    assert os.path.isfile(str(theme_dir / 'macros.html'))


def test_fails_outside_project_dir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(create_theme, ['mytheme'])

    assert result.exit_code != 0
    assert "create-theme must be executed from project dir" in result.output
