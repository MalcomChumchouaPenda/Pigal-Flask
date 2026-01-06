
import click
from . import commands



@click.group()
def cli():
    """Pigal command group"""
    
cli.add_command(commands.create_project)
cli.add_command(commands.create_frontend)
cli.add_command(commands.create_backend)
