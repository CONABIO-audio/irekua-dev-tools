import os
import sys
import venv
import shlex
import shutil
import subprocess
from subprocess import Popen, PIPE
from threading import Thread
from urllib.parse import urlparse
from urllib.request import urlretrieve
from contextlib import contextmanager

import click


def get_venv_path(target, name, venvs_dir=None):
    if venvs_dir is None:
        venvs_dir = '.venvs'

    return os.path.join(target, venvs_dir, name)


def has_venv(target, name, venvs_dir='.venvs'):
    path = get_venv_path(target, name, venvs_dir=venvs_dir)
    return os.path.exists(path)


def create_venv(target, name, venvs_dir=None, verbose=True):
    path = get_venv_path(target, name, venvs_dir=venvs_dir)

    if verbose:
        message = '[...] Creating virtual environment for {}'.format(name)
        click.secho(message, fg='cyan')

    try:
        subprocess.run(['/usr/local/bin/python3', '-m', 'venv', path])
    except Exception as error:
        message = f'[!!] Error while creating virtual environment. Error {error}'
        click.secho(message, fg='red')
        sys.exit()

    if verbose:
        message = '[+] Virtual environment for {} created'.format(name)
        click.secho(message, fg='green')


def remove_venv(target, name, venvs_dir=None):
    path = get_venv_path(target, name, venvs_dir=venvs_dir)
    if os.path.exists(path):
        shutil.rmtree(path)


@contextmanager
def activate_venv(target, name, venvs_dir=None):
    venv_path = get_venv_path(target, name, venvs_dir=venvs_dir)
    activate_path = os.path.join(venv_path, 'bin', 'activate')

    if not os.path.exists(activate_path):
        message = (
            'App {name} not installed. Please run:  irekua dev install'
            ' {name}'.format(name=name))
        raise click.ClickException(message)

    command_string = "env -i bash -c 'source {} && env'".format(activate_path)

    old_env = {}
    try:
        command = shlex.split(command_string)
        proc = subprocess.Popen(command, stdout = subprocess.PIPE)

        for line in proc.stdout:
            (key, _, value) = line.decode().partition("=")
            if key in os.environ:
                old_env[key] = os.environ[key]

            os.environ[key] = value
        proc.communicate()

        yield
    finally:
        for key, value in old_env.items():
            os.environ[key] = value


def run_python(
        target,
        name,
        arguments,
        venvs_dir=None,
        capture=False,
        stdout=True,
        stderr=True):
    venv_path = get_venv_path(target, name, venvs_dir=venvs_dir)
    python_path = os.path.join(venv_path, 'bin', 'python')

    with activate_venv(target, name, venvs_dir=venvs_dir):
        commands = [
            python_path
        ] + arguments

        try:
            if not capture:
                stdout = None if stdout else subprocess.PIPE
                stderr = None if stderr else subprocess.STDOUT

                return subprocess.run(commands, stderr=stderr, stdout=stdout)

            return subprocess.check_output(commands)

        except Exception as error:
            message = f'[!!] Error while running python in virtual environment. Error {error}'
            click.secho(message, fg='red')
            sys.exit()


def run_pip(
        target,
        name,
        arguments,
        venvs_dir=None,
        capture=False,
        stdout=True,
        stderr=True):

    commands = [
        '-m',
        'pip',
    ] + arguments

    return run_python(
        target,
        name,
        commands,
        capture=capture,
        stderr=stderr,
        stdout=stdout,
        venvs_dir=venvs_dir)


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
