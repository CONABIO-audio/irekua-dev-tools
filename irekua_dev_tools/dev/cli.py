import click
import time

from irekua_dev_tools.utils import check_app_name

from .install import install_app
from .install import update_app
from .install import is_installed
from .install import run_django_server
from .install import run_app_shell
from .install import run_manage
from .install import run_venv_python
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
@click.argument('name', type=str)
@click.option('--reinstall', '-r', is_flag=True)
def install(ctx, name, reinstall):
    target = ctx.obj['target']
    venvs_dir = ctx.obj['venvs_dir']
    repository_info = ctx.obj['repository_info']

    check_app_name(name, repository_info)

    dependencies = repository_info[name]['dependencies']
    install_app(target, name, dependencies, venvs_dir=venvs_dir, reinstall=reinstall)


@cli.command()
@click.pass_context
@click.argument('name', type=str)
@click.option('--install', '-i', is_flag=True)
def update(ctx, name, install):
    target = ctx.obj['target']
    venvs_dir = ctx.obj['venvs_dir']
    repository_info = ctx.obj['repository_info']

    check_app_name(name, repository_info)

    dependencies = repository_info[name]['dependencies']
    if not is_installed(target, name, dependencies, venvs_dir=venvs_dir):
        if install:
            install_app(target, name, dependencies, venvs_dir=venvs_dir)
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
@click.argument('name', type=str)
@click.option('--install', '-i', is_flag=True)
def shell(ctx, name, install):
    target = ctx.obj['target']
    venvs_dir = ctx.obj['venvs_dir']
    repository_info = ctx.obj['repository_info']

    check_app_name(name, repository_info)

    dependencies = repository_info[name]['dependencies']
    if not is_installed(target, name, dependencies, venvs_dir=venvs_dir):
        if not install:
            message = (
                'App {name} is not installed. Please run:  irekua dev install '
                '{name}'.format(name=name))
            click.secho(message, fg='red')
            return

        dependencies = repository_info[name]['dependencies']
        install_app(target, name, dependencies, venvs_dir=venvs_dir)

    run_app_shell(target, name, venvs_dir=venvs_dir)


@cli.command()
@click.pass_context
@click.argument('name', type=str)
@click.option('--install', '-i', is_flag=True)
@click.option('--update', '-u', is_flag=True)
@click.option('--port', '-p', type=str, default='8000')
def start(ctx, name, install, update, port):
    target = ctx.obj['target']
    venvs_dir = ctx.obj['venvs_dir']
    repository_info = ctx.obj['repository_info']

    check_app_name(name, repository_info)

    dependencies = repository_info[name]['dependencies']
    if not is_installed(target, name, dependencies, venvs_dir=venvs_dir):
        if not install:
            message = (
                'App {name} is not installed. Please run irekua dev install '
                ' {name}'.format(name=name))
            click.secho(message, fg='red')
            return

        dependencies = repository_info[name]['dependencies']
        install_app(target, name, dependencies, venvs_dir=venvs_dir)

    if update:
        update_app(target, name, venvs_dir=venvs_dir, stdout=False)
        click.secho('App {} succesfully updated'.format(name), fg='green')

    django_thread = run_django_server(
        target, name, venvs_dir=venvs_dir, port=port)
    dependencies = repository_info[name]['dependencies']
    observers = observe_app_dependencies(
        target, name, dependencies, venvs_dir=venvs_dir)

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


@cli.command(context_settings={"ignore_unknown_options": True})
@click.pass_context
@click.argument('name', type=str)
@click.argument('command', nargs=1)
@click.argument('extra', nargs=-1, required=False)
def manage(ctx, name, command, extra):
    target = ctx.obj['target']
    venvs_dir = ctx.obj['venvs_dir']
    repository_info = ctx.obj['repository_info']

    check_app_name(name, repository_info)

    run_manage(target, name, command, extra, venvs_dir=venvs_dir)


@cli.command(context_settings={"ignore_unknown_options": True})
@click.pass_context
@click.argument('name', type=str)
@click.argument('extra', nargs=-1, required=False)
def python(ctx, name, extra):
    target = ctx.obj['target']
    venvs_dir = ctx.obj['venvs_dir']
    repository_info = ctx.obj['repository_info']

    check_app_name(name, repository_info)

    run_venv_python(target, name, extra, venvs_dir=venvs_dir)
