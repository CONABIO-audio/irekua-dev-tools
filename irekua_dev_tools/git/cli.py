import threading
import click

from irekua_dev_tools.repositories import REPOSITORY_INFO

from .git import download_repository
from .git import update_repository
from .git import check_repository


@click.group(name="git")
@click.pass_context
@click.option('--origin', '-o', default='origin')
@click.option('--branch', '-b', default='master')
def cli(ctx, origin, branch):
    """Commands to manage git repositories"""
    config = ctx.obj['config']['git']
    ctx.obj['origin'] = config.get('origin', origin)
    ctx.obj['branch'] = config.get('branch', branch)


@cli.command()
@click.pass_context
@click.argument('name', type=click.Choice(REPOSITORY_INFO.keys()))
@click.option('--force', '-f', is_flag=True)
def download(ctx, name, force):
    """Download a single irekua/selia app repository"""
    target = ctx.obj['target']

    download_repository(name, target, force=force)


@cli.command()
@click.pass_context
@click.option('--force', '-f', is_flag=True)
def download_all(ctx, force):
    """Download all irekua/selia app repositories"""
    target = ctx.obj['target']

    for name in REPOSITORY_INFO.keys():
        download_repository(name, target, force=force)


@cli.command()
@click.pass_context
@click.argument('name', type=click.Choice(REPOSITORY_INFO.keys()))
@click.option('--download', '-d', is_flag=True)
def update(ctx, name, download):
    """Update a single irekua/selia app repository"""
    target = ctx.obj['target']
    origin = ctx.obj['origin']
    branch = ctx.obj['branch']

    update_repository(
        name,
        target,
        branch=branch,
        origin=origin,
        download=download)


@cli.command()
@click.pass_context
@click.option('--download', '-d', is_flag=True)
def update_all(ctx, download):
    """Update all irekua/selia app repositories"""
    target = ctx.obj['target']
    origin = ctx.obj['origin']
    branch = ctx.obj['branch']

    threads = [
        threading.Thread(
            target=update_repository,
            args=[name, target, branch, origin, download])
        for name in REPOSITORY_INFO.keys()]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


@cli.command()
@click.pass_context
@click.argument('name', type=click.Choice(REPOSITORY_INFO.keys()))
def check(ctx, name):
    """Check the status of a single irekua/selia app repository"""
    target = ctx.obj['target']
    origin = ctx.obj['origin']
    branch = ctx.obj['branch']

    check_repository(name, target, origin=origin, branch=branch)


@cli.command()
@click.pass_context
@click.option('--silent', '-s', is_flag=True)
def check_all(ctx, silent):
    """Check the status of all irekua/selia app repository"""
    target = ctx.obj['target']
    origin = ctx.obj['origin']
    branch = ctx.obj['branch']

    threads = [
        threading.Thread(
            target=check_repository,
            args=[name, target, silent, origin, branch])
        for name in REPOSITORY_INFO.keys()]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
