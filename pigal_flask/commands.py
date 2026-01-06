
import os
import click
import zipfile as zpf
import shutil
from cookiecutter.main import cookiecutter
from .exceptions import InvalidCommandContext, InvalidThemeFile


template_dir = os.path.dirname(__file__)
theme_required_paths = (
    'static/',
    'templates/layouts/',
    'templates/layouts/auth.jinja',
    'templates/layouts/dashboard.jinja',
    'templates/layouts/landing.jinja',
    'templates/home/',
    'templates/home/login.jinja',
    'templates/home/dashboard.jinja',
    'templates/home/index.jinja',
    'templates/demo/',
)


@click.command('create-project')
@click.argument('name')
@click.argument('theme')
def create_project(name, theme):
    """Create new Pigal project
    """
    extra = {'project_name': name, 'project_theme': theme}
    template = os.path.join(template_dir, 'cookiecutter_project')
    cookiecutter(template, no_input=True, extra_context=extra)

    with zpf.ZipFile(theme, 'r') as file:
        # check zipfile
        for required_path in theme_required_paths:
            found = False
            for file_name in file.namelist():
                if required_path in file_name:
                    found = True
                    break
            if not found:
                theme_name = os.path.basename(theme)
                msg = f'{theme_name} does not contain valid theme'
                raise InvalidThemeFile(msg)

        # extract files into project
        output_dir = os.path.abspath(f'./{name}/app')
        file.extractall(output_dir)
    
    # move home and example directories
    for key in ('home', 'demo'):
        src_dir = f'./{name}/app/templates/{key}'
        src_dir = os.path.abspath(src_dir)
        if os.path.isdir(src_dir):
            dest_dir = f'./{name}/frontends/{key}/templates/{key}'
            dest_dir = os.path.abspath(dest_dir)
            if os.path.isdir(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.move(src_dir, dest_dir)


@click.command('create-frontend')
@click.argument('domain')
def create_frontend(domain):
    """Create new frontend
    """
    if os.path.basename(os.getcwd()) != 'frontends':
        msg = "This command must be executed from frontends directory"
        raise InvalidCommandContext(msg)
    
    extra = {'project_name': domain}
    template = os.path.join(template_dir, 'cookiecutter_frontend')
    cookiecutter(template, no_input=True, extra_context=extra)


@click.command('create-backend')
@click.argument('domain')
@click.argument('version')
def create_backend(domain, version):
    """Create new backend
    """
    if os.path.basename(os.getcwd()) != 'backends':
        msg = "This command must be executed from backends directory"
        raise InvalidCommandContext(msg)

    name = f"{domain}_v{version.replace('.', '_')}"
    extra = {'project_name': name}
    template = os.path.join(template_dir, 'cookiecutter_backend')
    cookiecutter(template, no_input=True, extra_context=extra)
    
    
