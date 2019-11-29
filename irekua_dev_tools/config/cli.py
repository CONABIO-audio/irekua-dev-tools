import click

from .utils import print_config
from .utils import restore_config
from .utils import backup_config
from .utils import update_config


@click.group(name='config')
def cli():
    """Configuration commands"""


@cli.command()
@click.pass_context
def show(ctx):
    print_config(ctx.obj['config'])


@cli.command()
def restore():
    restore_config()


@cli.command()
@click.option('--origin', '-o')
@click.option('--branch', '-b')
@click.option('--working-directory', '-w', 'working_directory')
@click.option('--config-file', '-c', 'config_file')
def set(origin, branch, working_directory, config_file):
    backup_config()
    update_config(
        working_directory=working_directory,
        config_file=config_file,
        origin=origin,
        branch=branch)

