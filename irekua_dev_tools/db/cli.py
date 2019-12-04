import click

from .utils import check_database
from .utils import setup_database
from .utils import delete_database
from .migrations import migrate_database


@click.group(name="db")
@click.pass_context
@click.option('--user', '-u')
@click.option('--host', '-h')
@click.option('--port', '-p')
@click.option('--password', '-k')
@click.option('--name', '-n')
@click.option('--venvs-dir', '-vd', 'venvs_dir')
def cli(ctx, user, host, port, password, name, venvs_dir):
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
    ctx.obj['venvs_dir'] = config['dev'].get('venvs_dir', venvs_dir)

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
    config = ctx.obj['db_config']
    repository_info = ctx.obj['repository_info']
    target = ctx.obj['target']
    venvs_dir = ctx.obj['venvs_dir']

    check_database(config, repository_info, target, venvs_dir=venvs_dir)


@cli.command()
@click.pass_context
@click.option('--force', '-f', is_flag=True)
def setup(ctx, force):
    config = ctx.obj['db_config']
    venvs_dir = ctx.obj['venvs_dir']
    repository_info = ctx.obj['repository_info']
    target = ctx.obj['target']

    if force:
        click.confirm('Are you sure you want to reset the database?', abort=True)

    setup_database(
        config,
        repository_info,
        target,
        venvs_dir=venvs_dir,
        force=force)


@cli.command()
@click.pass_context
def delete(ctx):
    if click.confirm('Are you sure you want to delete the database?'):
        delete_database(ctx.obj['db_config'])



@cli.command()
@click.pass_context
def migrate(ctx):
    venvs_dir = ctx.obj['venvs_dir']
    repository_info = ctx.obj['repository_info']
    target = ctx.obj['target']

    migrate_database(repository_info, target, venvs_dir=venvs_dir)
