
import os
import pytest
from click.testing import CliRunner
from pigal_flask.commands import create_pages


@pytest.fixture
def fake_dir(tmpdir):
    project_dir = tmpdir / 'test'
    project_dir.mkdir()
    pages_dir = project_dir / 'pages'
    pages_dir.mkdir()
    return pages_dir.strpath


def test_create_basic_structure(change_dir, fake_dir):
    runner = CliRunner()
    with change_dir(fake_dir):
        result = runner.invoke(create_pages, ['foo'])

    test_dir = os.path.join(fake_dir, 'foo')
    assert result.exit_code == 0
    assert os.path.isdir(test_dir)
    assert os.path.isdir(os.path.join(test_dir, 'static'))
    assert os.path.isdir(os.path.join(test_dir, 'templates'))
    assert os.path.isfile(os.path.join(test_dir, '__init__.py'))
    assert os.path.isfile(os.path.join(test_dir, 'forms.py'))
    assert os.path.isfile(os.path.join(test_dir, 'routes.py'))

