
import os
import pytest
from click.testing import CliRunner
from pigal_flask.commands import create_service


@pytest.fixture
def fake_dir(tmpdir):
    project_dir = tmpdir / 'test'
    project_dir.mkdir()
    services_dir = project_dir / 'services'
    services_dir.mkdir()
    return services_dir.strpath


def test_create_basic_structure(change_dir, fake_dir):
    runner = CliRunner()
    with change_dir(fake_dir):
        result = runner.invoke(create_service, ['foo', '1.0'])

    test_dir = os.path.join(fake_dir, 'foo_v1_0')
    assert result.exit_code == 0
    assert os.path.isdir(test_dir)
    assert os.path.isdir(os.path.join(test_dir, 'store'))
    assert os.path.isfile(os.path.join(test_dir, '__init__.py'))
    assert os.path.isfile(os.path.join(test_dir, 'models.py'))
    assert os.path.isfile(os.path.join(test_dir, 'routes.py'))
    assert os.path.isfile(os.path.join(test_dir, 'utils.py'))


@pytest.mark.parametrize('name', ['foo', 'service', 'pages'])
def test_cannot_create_service_outside_services(change_dir, tmpdir, name):
    test_dir = tmpdir / name
    test_dir.mkdir()
    runner = CliRunner()
    with change_dir(test_dir.strpath):
        result = runner.invoke(create_service, ['foo', '1.0'])

    assert result.exit_code != 0
    assert "This command must be executed from \\services" in result.output
