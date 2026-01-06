
import os
import pytest
from click.testing import CliRunner
from pigal_flask.commands import create_frontend


@pytest.fixture
def fake_dir(tmpdir):
    project_dir = tmpdir / 'test'
    project_dir.mkdir()
    frontends_dir = project_dir / 'frontends'
    frontends_dir.mkdir()
    return frontends_dir.strpath


def test_create_basic_structure(change_dir, fake_dir):
    runner = CliRunner()
    with change_dir(fake_dir):
        result = runner.invoke(create_frontend, ['foo'])

    test_dir = os.path.join(fake_dir, 'foo')
    assert result.exit_code == 0
    assert os.path.isdir(test_dir)
    assert os.path.isdir(os.path.join(test_dir, 'static'))
    assert os.path.isdir(os.path.join(test_dir, 'templates'))
    assert os.path.isdir(os.path.join(test_dir, 'templates', 'foo'))
    assert os.path.isfile(os.path.join(test_dir, '__init__.py'))
    assert os.path.isfile(os.path.join(test_dir, 'forms.py'))
    assert os.path.isfile(os.path.join(test_dir, 'routes.py'))


@pytest.mark.parametrize('name', ['foo', 'frontend', 'backends'])
def test_cannot_create_frontend_outside_frontends(change_dir, tmpdir, name):
    test_dir = tmpdir / name
    test_dir.mkdir()
    runner = CliRunner()
    with change_dir(test_dir.strpath):
        result = runner.invoke(create_frontend, ['foo'])

    assert result.exit_code != 0
    assert "This command must be executed from frontends directory" in result.output

