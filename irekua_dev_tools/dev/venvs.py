import os
import subprocess

import click


def get_venv_path(target, name, venvs_dir=None):
    if venvs_dir is None:
        venvs_dir = '.venvs'

    return os.path.join(target, venvs_dir, name)


def has_venv(target, name, venvs_dir='.venvs'):
    path = get_venv_path(target, name, venvs_dir=venvs_dir)
    return os.path.exists(path)


def create_venv(target, name, python='python3', venvs_dir=None, verbose=True):
    path = get_venv_path(target, name, venvs_dir=venvs_dir)

    if verbose:
        message = '[...] Creating virtual environment for {}'.format(name)
        click.secho(message, fg='cyan')

    subprocess.run(['virtualenv', '-p', python, path])

    if verbose:
        message = '[+] Virtual environment for {} created'.format(name)
        click.secho(message, fg='green')


def run_python(
        target,
        name,
        arguments,
        venvs_dir=None,
        capture=False,
        stdout=True,
        stderr=True):
    venv_path = get_venv_path(target, name, venvs_dir=venvs_dir)
    python_bin_path = os.path.join(venv_path, 'bin', 'python')

    if not capture:
        stdout = None if stdout else subprocess.PIPE
        stderr = None if stderr else subprocess.STDOUT
        return subprocess.run(
            [python_bin_path, *arguments],
            stderr=stderr,
            stdout=stdout)

    return subprocess.run(
        [python_bin_path, *arguments],
        capture_output=capture).stdout


def run_pip(
        target,
        name,
        arguments,
        venvs_dir=None,
        capture=False,
        stdout=True,
        stderr=True):
    venv_path = get_venv_path(target, name, venvs_dir=venvs_dir)
    pip_bin_path = os.path.join(venv_path, 'bin', 'pip')

    if not capture:
        stdout = None if stdout else subprocess.PIPE
        stderr = None if stderr else subprocess.STDOUT
        return subprocess.run(
            [pip_bin_path, *arguments],
            stdout=stdout,
            stderr=stderr)

    return subprocess.run(
        [pip_bin_path, *arguments],
        capture_output=capture).stdout


def install_packages(
        target,
        name,
        packages,
        venvs_dir=None,
        stdout=True,
        stderr=True):
    arguments = ['install', '-y', '-U'] + packages
    run_pip(target, name, arguments,
            venvs_dir=venvs_dir, stdout=stdout, stderr=stderr)
