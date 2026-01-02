
import click
from . import commands


@click.group()
def cli():
    pass

cli.add_command(commands.create_project)
cli.add_command(commands.create_pages)
cli.add_command(commands.create_service)
