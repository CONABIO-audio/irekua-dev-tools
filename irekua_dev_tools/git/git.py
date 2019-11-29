import subprocess
import os
import click
import shutil

from irekua_dev_tools.repositories import REPOSITORY_INFO


def get_target_directory(name, target):
    working_directory = os.getcwd()
    target = os.path.join(working_directory, target, name, '')

    if not os.path.exists(target):
        os.makedirs(target)

    return target


def is_git_repository(path):
    git_directory = os.path.join(path, '.git')
    return os.path.exists(git_directory)


def download_repository(name, target, force=False):
    target_directory = get_target_directory(name, target)

    if is_git_repository(target_directory):
        if not force:
            message = 'Repository for {} has already been downloaded'.format(name)
            click.secho(message, fg='yellow')
            return

        shutil.rmtree(target_directory)

    source = REPOSITORY_INFO[name]['git']
    subprocess.call(['git', 'clone', source, target_directory])

    message = 'Repository for {} succesfully downloaded'.format(name)
    click.secho(message, fg='green')


def update_repository(name, target, branch='master', origin='origin', download=False):
    target_directory = get_target_directory(name, target)

    if not is_git_repository(target_directory):
        if download:
            download_repository(name, target, force=True)
            return

        message = (
                'Repository for {name} has not been downloaded yet. Please run: '
            ' irekua git download {name}'.format(name=name))
        click.secho(message, fg='red')
        return

    subprocess.call(
        ['git', '-C', target_directory, 'pull', origin, branch],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)

    message = 'Repository for {} succesfully updated'.format(name)
    click.secho(message, fg='green')


def check_repository(name, target, silent=False, origin='origin', branch='master'):
    target_directory = get_target_directory(name, target)

    if not is_git_repository(target_directory):
        message = (
                '[-] [DOWNLOAD] Repository for {name} has not been downloaded.'
                ' Please run: irekua git download {name}'.format(name=name))
        click.secho(message, fg='red')
        return

    if needs_update(target_directory, origin=origin, branch=branch):
        message = (
            '[+] [UPDATE] Repository for {name} needs an update. Please run: '
            'irekua git update {name}'.format(name=name))
        click.secho(message, fg='yellow')
        return

    if has_changes(target_directory):
        message = (
            '[+] [COMMIT] Repository for {name} has pending changes. Check '
            'full status and commit'.format(name=name))
        click.secho(message, fg='yellow')
        return

    if not silent:
        message = (
                '[=] Repository for {name} is up to date and has no '
                'changes.'.format(name=name))
        click.secho(message, fg='green')


def has_changes(target_directory):
    status = subprocess.check_output(
        ['git', '-C', target_directory, 'status', '-s'])
    return bool(status)


def needs_update(target_directory, origin='origin', branch='master'):
    status = subprocess.check_output(
        ['git', '-C', target_directory, 'fetch', '--dry-run', origin, branch],
        stderr=subprocess.STDOUT)
    lines = str(status).split('\\n')
    return len(lines) > 3
