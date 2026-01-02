
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


@click.group()
def cli():
    pass

cli.add_command(create_project)


if __name__ == "__main__":
    cli()