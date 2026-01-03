
import os
import click
import zipfile as zpf
import shutil
from cookiecutter.main import cookiecutter


template_dir = os.path.dirname(__file__)


@click.command('create-project')
@click.argument('name')
@click.argument('theme')
def create_project(name, theme):
    extra = {'project_name': name, 'project_theme': theme}
    template = os.path.join(template_dir, 'cookiecutter_project')
    cookiecutter(template, no_input=True, extra_context=extra)
    with zpf.ZipFile(theme, 'r') as file:
        output_dir = os.path.abspath(f'./{name}/app')
        file.extractall(output_dir)
    
    # move home and example directories
    for key in ('home', 'examples'):
        src_dir = os.path.abspath(f'./{name}/app/templates/{key}')
        dest_dir = os.path.abspath(f'./{name}/pages/home/templates/{key}')
        if os.path.isdir(src_dir):
            if os.path.isdir(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.move(src_dir, dest_dir)


@click.command('create-pages')
@click.argument('domain')
def create_pages(domain):
    if os.path.basename(os.getcwd()) != 'pages':
        msg = "This command must be executed from \pages"
        raise click.ClickException(msg)
    
    extra = {'project_name': domain}
    template = os.path.join(template_dir, 'cookiecutter_pages')
    cookiecutter(template, no_input=True, extra_context=extra)


@click.command('create-service')
@click.argument('domain')
@click.argument('version')
def create_service(domain, version):
    if os.path.basename(os.getcwd()) != 'services':
        msg = "This command must be executed from \\services"
        raise click.ClickException(msg)

    name = f"{domain}_v{version.replace('.', '_')}"
    extra = {'project_name': name}
    template = os.path.join(template_dir, 'cookiecutter_service')
    cookiecutter(template, no_input=True, extra_context=extra)
    