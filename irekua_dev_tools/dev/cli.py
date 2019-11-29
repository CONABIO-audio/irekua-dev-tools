import click
import time

from irekua_dev_tools.repositories import REPOSITORY_INFO

from .install import install_app
from .install import update_app
from .install import is_installed
from .install import run_django_server
from .watch import observe_app_dependencies


@click.group(name="dev")
@click.pass_context
@click.option('--venvs-dir', '-vd', 'venvs_dir')
def cli(ctx, venvs_dir):
    """Commands to setup development environment"""
    config = ctx.obj['config']['dev']
    ctx.obj['venvs_dir'] = config.get('venvs_dir', venvs_dir)


@cli.command()
@click.pass_context
@click.argument('name', type=click.Choice(REPOSITORY_INFO.keys()))
@click.option('--install', '-i', is_flag=True)
def install(ctx, name, install):
    target = ctx.obj['target']
    venvs_dir = ctx.obj['venvs_dir']

    install_app(target, name, venvs_dir=venvs_dir)


@cli.command()
@click.pass_context
@click.argument('name', type=click.Choice(REPOSITORY_INFO.keys()))
def update(ctx, name):
    target = ctx.obj['target']
    venvs_dir = ctx.obj['venvs_dir']

    if not is_installed(target, name, venvs_dir=venvs_dir):
        if install:
            install_app(target, name, venvs_dir=venvs_dir)
            click.secho('App {} succesfully updated'.format(name), fg='green')
            return

        message = (
            'App {name} is not installed. Please run irekua dev install '
            ' {name}'.format(name=name))
        click.secho(message, fg='red')
        return

    update_app(target, name, venvs_dir=venvs_dir)
    click.secho('App {} succesfully updated'.format(name), fg='green')


@cli.command()
@click.pass_context
@click.argument('name', type=click.Choice(REPOSITORY_INFO.keys()))
@click.option('--install', '-i', is_flag=True)
@click.option('--update', '-u', is_flag=True)
@click.option('--port', '-p', type=str, default='8000')
def start(ctx, name, install, update, port):
    target = ctx.obj['target']
    venvs_dir = ctx.obj['venvs_dir']

    if not is_installed(target, name, venvs_dir=venvs_dir):
        if not install:
            message = (
                    'App {name} is not installed. Please run irekua dev install '
                    ' {name}'.format(name=name))
            click.secho(message, fg='red')
            return

        install_app(target, name, venvs_dir=venvs_dir)

    if update:
        update_app(target, name, venvs_dir=venvs_dir, output=False)
        click.secho('App {} succesfully updated'.format(name), fg='green')

    django_thread = run_django_server(
        target, name, venvs_dir=venvs_dir, port=port)
    observers = observe_app_dependencies(
        target, name, venvs_dir=venvs_dir)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
        click.secho('Development servers terminated', fg='red')

    for observer in observers:
        observer.join()
    django_thread.join()
