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


@cli.command(name='set')
@click.option('--origin', '-o')
@click.option('--branch', '-b')
@click.option('--working-directory', '-w', 'working_directory')
@click.option('--config-file', '-c', 'config_file')
@click.option('--db-host', '-dh', 'db_host')
@click.option('--db-name', '-dn', 'db_name')
@click.option('--db-user', '-du', 'db_user')
@click.option('--db-port', '-dp', 'db_port')
@click.option('--db-password', '-dk', 'db_password')
def set_config(
        origin,
        branch,
        working_directory,
        config_file,
        db_host,
        db_name,
        db_user,
        db_port,
        db_password):
    backup_config()
    update_config(
        working_directory=working_directory,
        config_file=config_file,
        origin=origin,
        branch=branch,
        db_host=db_host,
        db_name=db_name,
        db_user=db_user,
        db_port=db_port,
        db_password=db_password)
