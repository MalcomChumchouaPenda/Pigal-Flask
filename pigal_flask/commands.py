import os
import click
import zipfile as zpf
import shutil
from cookiecutter.main import cookiecutter
from .exceptions import InvalidCommandContext, InvalidThemeFile


template_dir = os.path.dirname(__file__)


@click.command("create-project")
@click.argument("name")
def create_project(name):
    """
    Create new project
    """
    extra = {"project_name": name}
    template = os.path.join(template_dir, "cookiecutter_project")
    cookiecutter(template, no_input=True, extra_context=extra)


@click.command("create-module")
@click.argument("name")
def create_module(name):
    """Create new module"""
    cur_dir = os.getcwd()
    modules_dir = os.path.join(cur_dir, "modules")
    if not os.path.isdir(modules_dir):
        msg = "create-module must be executed from project dir"
        raise InvalidCommandContext(msg)

    extra = {"module_name": name}
    template = os.path.join(template_dir, "cookiecutter_module")
    cookiecutter(template, no_input=True, extra_context=extra)


@click.command("import-theme")
@click.argument("path")
def import_theme(path):
    """Import new theme"""
    cur_dir = os.getcwd()
    theme_dir = os.path.join(cur_dir, "app", "theme")
    if not os.path.isdir(theme_dir):
        msg = "import-theme must be executed from a project dir"
        raise InvalidCommandContext(msg)
    for name in ("static", "templates"):
        to_clean = os.path.join(theme_dir, name)
        shutil.rmtree(to_clean, ignore_errors=True)
    with zpf.ZipFile(path, "r") as archive:
        archive.extractall(theme_dir)
