
import os
import click
import zipfile as zpf
import shutil
from cookiecutter.main import cookiecutter
from .exceptions import InvalidCommandContext, InvalidThemeFile


template_dir = os.path.dirname(__file__)


@click.command('create-project')
@click.argument('name')
def create_project(name):
    """
    Create new project
    """
    extra = {'project_name': name}
    template = os.path.join(template_dir, 'cookiecutter_project')
    cookiecutter(template, no_input=True, extra_context=extra)


@click.command('create-module')
@click.argument('name')
def create_module(name):
    """Create new module
    """
    cur_dir = os.getcwd()
    modules_dir = os.path.join(cur_dir, 'modules')
    if not os.path.isdir(modules_dir):
        msg = "create-module must be executed from project dir"
        raise InvalidCommandContext(msg)

    extra = {'module_name': name}
    template = os.path.join(template_dir, 'cookiecutter_module')
    cookiecutter(template, no_input=True, extra_context=extra)


@click.command('create-theme')
@click.argument('name')
def create_theme(name):
    """Create new theme
    """
    cur_dir = os.getcwd()
    themes_dir = os.path.join(cur_dir, 'themes')
    if not os.path.isdir(themes_dir):
        msg = "create-theme must be executed from project dir"
        raise InvalidCommandContext(msg)

    extra = {'theme_name': name}
    template = os.path.join(template_dir, 'cookiecutter_theme')
    cookiecutter(template, no_input=True, extra_context=extra)


