import glob
import os
import threading
import click

from .venvs import create_venv
from .venvs import has_venv
from .venvs import run_python
from .venvs import run_pip
from .venvs import get_venv_path
from .venvs import remove_venv


def is_installed(target, name, dependencies, venvs_dir=None):
    venv_path = get_venv_path(target, name, venvs_dir=venvs_dir)

    if not os.path.exists(venv_path):
        return False

    packages_glob = os.path.join(
        venv_path,
        'lib',
        '**',
        'site-packages',
        '*.egg')

    packages_files = [
        os.path.basename(package).split('-')[0]
        for package in glob.glob(packages_glob)
    ]

    for dependency in dependencies:
        if not dependency.replace('-', '_') in packages_files:
            return False

    return True


def install_app(target, name, dependencies, venvs_dir=None, reinstall=False):
    if reinstall:
        remove_venv(target, name, venvs_dir=venvs_dir)

    if not has_venv(target, name, venvs_dir=venvs_dir):
        create_venv(target, name, venvs_dir=venvs_dir)

    click.secho('Installing app {}'.format(name), fg='cyan')
    for dependency in dependencies:
        install_dependency(target, name, dependency, venvs_dir=venvs_dir)

    update_app(target, name, venvs_dir=venvs_dir)


def update_app(target, name, venvs_dir=None, stdout=True, stderr=True):
    install_dependency(
        target,
        name,
        name,
        venvs_dir=venvs_dir,
        stdout=stdout,
        stderr=stderr)
    create_requirements(target, name, venvs_dir=venvs_dir)


def install_dependency(
        target,
        name,
        dependency_name,
        venvs_dir=None,
        stdout=True,
        stderr=True):
    click.secho(
        '[...] Installing app {} dependency: {}'.format(name, dependency_name),
        fg='cyan')
    setup_file = os.path.join(target, dependency_name, 'setup.py')
    arguments = [setup_file, 'install']
    run_python(
        target,
        name,
        arguments,
        venvs_dir=venvs_dir,
        stdout=stdout,
        stderr=stderr)
    click.secho(
        '[+] {} dependency {} installed'.format(name, dependency_name),
        fg='green')


def create_requirements(target, name, venvs_dir=None):
    arguments = ['freeze']
    output = run_pip(target, name, arguments, venvs_dir=venvs_dir, capture=True)

    requirements = output.decode('utf-8').split('\n')
    file_path = os.path.join(target, name, 'requirements.txt')
    with open(file_path, 'w') as rfile:
        for requirement in requirements:
            if name not in requirement:
                rfile.write(requirement + '\n')


def run_django_server(target, name, venvs_dir=None, port=8000):
    module_name = os.path.join(target, name, 'manage.py')

    if not os.path.exists(module_name):
        message = 'App {} is not a django app'.format(name)
        click.secho(message, fg='red')
        return

    arguments = [module_name, 'runserver', port]
    django_server_thread = threading.Thread(
        target=run_python,
        args=[target, name, arguments, venvs_dir])
    django_server_thread.start()
    return django_server_thread


def run_app_shell(target, name, venvs_dir=None):
    module_name = os.path.join(target, name, 'manage.py')

    if not os.path.exists(module_name):
        message = 'App {} is not a django app'.format(name)
        click.secho(message, fg='red')
        return

    arguments = [module_name, 'shell']
    run_python(target, name, arguments, venvs_dir=venvs_dir)


def run_manage(
        target,
        name,
        command,
        extra,
        venvs_dir=None,
        stderr=True,
        stdout=True):
    module_name = os.path.join(target, name, 'manage.py')

    if not os.path.exists(module_name):
        message = 'App {} is not a django app'.format(name)
        click.secho(message, fg='red')
        return

    arguments = [module_name, command]
    if extra:
        if isinstance(extra, (tuple, list)):
            arguments += list(extra)
        else:
            arguments.append(extra)

    return run_python(
        target,
        name,
        arguments,
        venvs_dir=venvs_dir,
        stderr=stderr,
        stdout=stdout)


def run_venv_python(
        target,
        name,
        extra,
        venvs_dir=None,
        stderr=True,
        stdout=True):

    return run_python(
        target,
        name,
        list(extra),
        venvs_dir=venvs_dir,
        stderr=stderr,
        stdout=stdout)
