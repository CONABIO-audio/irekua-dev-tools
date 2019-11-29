import click

from .utils import check_database
from .utils import setup_database
from .utils import delete_database


@click.group(name="db")
@click.pass_context
@click.option('--user', '-u')
@click.option('--host', '-h')
@click.option('--port', '-p')
@click.option('--password', '-k')
@click.option('--name', '-n')
def cli(ctx, user, host, port, password, name):
    """Commands for database configuration"""
    config = ctx.obj['config']
    if user is None:
        user = config['db']['user']
    if host is None:
        host = config['db']['host']
    if port is None:
        port = config['db']['port']
    if password is None:
        password = config['db']['password']
    if name is None:
        name = config['db']['name']

    ctx.obj['db_config'] = {
        'user': user,
        'host': host,
        'port': port,
        'password': password,
        'name': name,
    }


@cli.command()
@click.pass_context
def check(ctx):
    check_database(ctx.obj['db_config'])


@cli.command()
@click.pass_context
@click.option('--force', '-f', is_flag=True)
def setup(ctx, force):
    if force:
        click.confirm('Are you sure you want to reset the database?', abort=True)

    setup_database(ctx.obj['db_config'], force=force)


@cli.command()
@click.pass_context
def delete(ctx):
    if click.confirm('Are you sure you want to delete the database?'):
        delete_database(ctx.obj['db_config'])
