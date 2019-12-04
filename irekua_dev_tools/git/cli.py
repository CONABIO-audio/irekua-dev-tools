import threading
import click

from irekua_dev_tools.utils import check_app_name

from .git import download_repository
from .git import update_repository
from .git import check_repository


@click.group(name="git")
@click.pass_context
@click.option('--origin', '-o', default='origin')
@click.option('--branch', '-b', default='master')
@click.option('--method', '-m', default='http')
def cli(ctx, origin, branch, method):
    """Commands to manage git repositories"""
    config = ctx.obj['config']['git']
    ctx.obj['origin'] = config.get('origin', origin)
    ctx.obj['branch'] = config.get('branch', branch)
    ctx.obj['method'] = config.get('method', method)


@cli.command()
@click.pass_context
@click.argument('name', type=str, required=False)
@click.option('--force', '-f', is_flag=True)
def download(ctx, name, force):
    """Download a single irekua/selia app repository"""
    target = ctx.obj['target']
    method = ctx.obj['method']
    repository_info = ctx.obj['repository_info']

    if not name:
        ctx.invoke(download_all, force=force)

    else:
        check_app_name(name, repository_info)

        download_repository(
            name,
            target,
            repository_info,
            method=method,
            force=force)


@cli.command()
@click.pass_context
@click.option('--force', '-f', is_flag=True)
def download_all(ctx, force):
    """Download all irekua/selia app repositories"""
    target = ctx.obj['target']
    method = ctx.obj['method']
    repository_info = ctx.obj['repository_info']

    for name in repository_info.keys():
        download_repository(
            name,
            target,
            repository_info,
            method=method,
            force=force)


@cli.command()
@click.pass_context
@click.argument('name', type=str, required=False)
@click.option('--download', '-d', is_flag=True)
def update(ctx, name, download):
    """Update a single irekua/selia app repository"""
    target = ctx.obj['target']
    origin = ctx.obj['origin']
    branch = ctx.obj['branch']
    method = ctx.obj['method']
    repository_info = ctx.obj['repository_info']

    if not name:
        ctx.invoke(update_all, download=download)

    else:
        check_app_name(name, repository_info)

        update_repository(
            name,
            target,
            repository_info,
            branch=branch,
            origin=origin,
            method=method,
            download=download)


@cli.command()
@click.pass_context
@click.option('--download', '-d', is_flag=True)
def update_all(ctx, download):
    """Update all irekua/selia app repositories"""
    target = ctx.obj['target']
    origin = ctx.obj['origin']
    branch = ctx.obj['branch']
    method = ctx.obj['method']
    repository_info = ctx.obj['repository_info']

    threads = [
        threading.Thread(
            target=update_repository,
            args=[
                name,
                target,
                repository_info,
                branch,
                origin,
                method,
                download])
        for name in repository_info.keys()]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


@cli.command()
@click.pass_context
@click.argument('name', type=str, required=False)
@click.option('--silent', '-s', is_flag=True)
def check(ctx, name, silent):
    """Check the status of a single irekua/selia app repository"""
    target = ctx.obj['target']
    origin = ctx.obj['origin']
    branch = ctx.obj['branch']
    repository_info = ctx.obj['repository_info']

    if not name:
        ctx.invoke(check_all, silent=silent)

    else:
        check_app_name(name, repository_info)

        check_repository(name, target, silent=silent, origin=origin, branch=branch)


@cli.command()
@click.pass_context
@click.option('--silent', '-s', is_flag=True)
def check_all(ctx, silent):
    """Check the status of all irekua/selia app repository"""
    target = ctx.obj['target']
    origin = ctx.obj['origin']
    branch = ctx.obj['branch']
    repository_info = ctx.obj['repository_info']

    threads = [
        threading.Thread(
            target=check_repository,
            args=[name, target, silent, origin, branch])
        for name in repository_info.keys()]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
