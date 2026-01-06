
import os
import pytest
import zipfile as zpf
from click.testing import CliRunner
from pigal_flask.commands import create_project


THEME_FILES = [
    ('static', 'css', 'style.css'),
    ('static', 'js', 'custom.js'),
    ('static', 'other.txt'),
    ('templates', 'layouts', 'landing.jinja'),
    ('templates', 'layouts', 'dashboard.jinja'),
    ('templates', 'layouts', 'auth.jinja'),
    ('templates', 'layouts', 'other.jinja'),
    ('templates', 'home', 'index.jinja'),
    ('templates', 'home', 'dashboard.jinja'),
    ('templates', 'home', 'login.jinja'),
    ('templates', 'home', 'other.jinja'),
    ('templates', 'demo', 'test1.jinja'),
    ('templates', 'demo', 'test2.jinja'),
]


def create_valid_theme(tmpdir):
    themezip = tmpdir / 'theme_1_0.zip'
    with zpf.ZipFile(themezip, 'w') as file:
        for filenames in THEME_FILES:
            arcname = '/'.join(filenames)
            file.writestr(arcname, 'test')            
    return themezip.strpath


def test_create_project_structure(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        result = runner.invoke(create_project, ['test', theme])

    project_path = os.path.join(tmpdir, 'test')
    assert result.exit_code == 0
    assert os.path.isdir(project_path)
    assert os.path.isdir(os.path.join(project_path, 'app'))
    assert os.path.isdir(os.path.join(project_path, 'pages'))
    assert os.path.isdir(os.path.join(project_path, 'services'))


def test_unzip_theme_static_into_app_dir(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    app_path = os.path.join(tmpdir, 'test', 'app')
    for file_names in THEME_FILES:
        if 'static' == file_names[0]:
            file_name = os.path.join(app_path, *file_names)
            assert os.path.isfile(file_name)


def test_unzip_theme_layouts_into_app_dir(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    app_path = os.path.join(tmpdir, 'test', 'app')
    for file_names in THEME_FILES:
        if 'layouts' == file_names[1]:
            file_name = os.path.join(app_path, *file_names)
            assert os.path.isfile(file_name)


def test_unzip_home_templates_into_pages(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    home_path = os.path.join(tmpdir, 'test', 'pages', 'home')
    for file_names in THEME_FILES:
        if 'home' == file_names[1]:
            file_name = os.path.join(home_path, *file_names)
            assert os.path.isfile(file_name)


def test_unzip_demo_templates_into_pages(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    demo_path = os.path.join(tmpdir, 'test', 'pages', 'demo')
    for file_names in THEME_FILES:
        if 'demo' == file_names[1]:
            file_name = os.path.join(demo_path, *file_names)
            assert os.path.isfile(file_name)
    

def test_create_app_structure(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    app_path = os.path.join(tmpdir, 'test', 'app')
    assert os.path.isfile(os.path.join(app_path, 'config.py'))
    assert os.path.isfile(os.path.join(app_path, 'extensions.py'))
    assert os.path.isfile(os.path.join(app_path, '__init__.py'))


def test_create_app_config_file(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    file_path = os.path.join(tmpdir, 'test', 'app', 'config.py')
    with open(file_path, 'rt') as file:
        code = file.read()
        assert 'class Config:' in code
        assert "    PIGAL_PROJECT_NAME = 'test'" in code


def test_create_app_extensions_file(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    file_path = os.path.join(tmpdir, 'test', 'app', 'extensions.py')
    with open(file_path, 'rt') as file:
        code = file.read()
        assert 'from pigal_flask import Pigal, PigalDb' in code
        assert 'db = PigalDb()' in code
        assert 'pigal = Pigal()' in code


def test_create_app_init_file(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    file_path = os.path.join(tmpdir, 'test', 'app', '__init__.py')
    with open(file_path, 'rt') as file:
        code = file.read()
        assert 'from flask import Flask' in code
        assert 'from .extensions import db, pigal' in code
        assert 'from .config import Config' in code
        assert 'app = Flask(__name__)' in code
        assert 'app.config.from_object(Config)' in code
        assert 'pigal.init_app(app)' in code


def test_create_pages_structure(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    pages_path = os.path.join(tmpdir, 'test', 'pages')
    assert os.path.isdir(os.path.join(pages_path, 'home'))
    assert os.path.isdir(os.path.join(pages_path, 'demo'))
    assert os.path.isfile(os.path.join(pages_path, '__init__.py'))


def test_create_default_home_page(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    home_path = os.path.join(tmpdir, 'test', 'pages', 'home')
    assert os.path.isdir(os.path.join(home_path, 'static'))
    assert os.path.isdir(os.path.join(home_path, 'templates'))
    assert os.path.isdir(os.path.join(home_path, 'templates', 'home'))
    assert os.path.isfile(os.path.join(home_path, 'forms.py'))
    assert os.path.isfile(os.path.join(home_path, 'routes.py'))


def test_create_theme_demo_page(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    demo_path = os.path.join(tmpdir, 'test', 'pages', 'demo')
    assert os.path.isdir(os.path.join(demo_path, 'static'))
    assert os.path.isdir(os.path.join(demo_path, 'templates'))
    assert os.path.isdir(os.path.join(demo_path, 'templates', 'demo'))
    assert os.path.isfile(os.path.join(demo_path, 'forms.py'))
    assert os.path.isfile(os.path.join(demo_path, 'routes.py'))


def test_create_services_structure(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    services_path = os.path.join(tmpdir, 'test', 'services')
    assert os.path.isdir(os.path.join(services_path, 'auth'))
    assert os.path.isfile(os.path.join(services_path, '__init__.py'))


def test_create_default_auth_service(tmpdir, change_dir):
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_valid_theme(tmpdir)
        runner.invoke(create_project, ['test', theme])

    auth_path = os.path.join(tmpdir, 'test', 'services', 'auth')
    assert os.path.isdir(os.path.join(auth_path, 'store'))
    assert os.path.isfile(os.path.join(auth_path, 'utils.py'))
    assert os.path.isfile(os.path.join(auth_path, 'models.py'))
    assert os.path.isfile(os.path.join(auth_path, 'routes.py'))


def create_invalid_theme(tmpdir, ignored):
    themezip = tmpdir / 'theme_2_0.zip'
    with zpf.ZipFile(themezip, 'w') as file:
        for filenames in THEME_FILES:
            arcname = '/'.join(filenames)
            if not ignored in arcname:
                file.writestr(arcname, 'test')            
    return themezip.strpath


@pytest.mark.parametrize('required', [
    'static/',
    'templates/layouts/',
    'templates/home/',
    'templates/demo/'
])
def test_requires_theme_with_specific_folder(tmpdir, change_dir, required):    
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_invalid_theme(tmpdir, required)
        result = runner.invoke(create_project, ['test', theme])

    assert result.exit_code != 0
    assert "theme_2_0.zip does not contain valid theme" in result.output
    

@pytest.mark.parametrize('required', [
    'templates/layouts/auth.jinja',
    'templates/layouts/dashboard.jinja',
    'templates/layouts/landing.jinja',
    'templates/home/login.jinja',
    'templates/home/dashboard.jinja',
    'templates/home/index.jinja',
])
def test_requires_theme_with_specific_file(tmpdir, change_dir, required):    
    runner = CliRunner()
    with change_dir(tmpdir):
        theme = create_invalid_theme(tmpdir, required)
        result = runner.invoke(create_project, ['test', theme])

    assert result.exit_code != 0
    assert "theme_2_0.zip does not contain valid theme" in result.output
