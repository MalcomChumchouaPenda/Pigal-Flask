
import os
import click
import zipfile as zpf
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


@click.command('create-pages')
@click.argument('domain')
def create_pages(domain):
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


@click.group()
def cli():
    pass

cli.add_command(create_project)
cli.add_command(create_pages)
cli.add_command(create_service)


if __name__ == "__main__":
    cli()