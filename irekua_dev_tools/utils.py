import os
import json
import shutil
import configparser

import click
from irekua_dev_tools import BASE_DIR


BASE_PATH = os.path.join(BASE_DIR, 'settings.ini')
BASE_DEPENDENCY_FILE = os.path.join(BASE_DIR, 'repositories.json')


def clear_target_directory(target, repository_info, silent=False):
    for name in repository_info.keys():
        dir_path = os.path.join(target, name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            message = (
                'Directory for {} succesfully removed ({})'.format(
                    name, dir_path))
            click.secho(message, fg='green')


def load_repository_info(method='update', repository_file=None):
    with open(BASE_DEPENDENCY_FILE, 'r') as json_file:
        base_repository_info = json.load(json_file)

    if not os.path.exists(repository_file):
        return base_repository_info

    with open(repository_file, 'r') as json_file:
        repository_info = json.load(json_file)

    if method == 'replace':
        return repository_info

    base_repository_info.update(repository_info)
    return base_repository_info


def get_working_directory(config):
    working_directory = config['irekua']['working_directory']
    working_directory = os.path.expanduser(working_directory)
    return working_directory


def load_config(path=None, aux_config=True):
    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())
    config.read(BASE_PATH)

    paths = []
    if aux_config:
        paths.append(config['irekua']['config_file'])
    if path is not None:
        paths.append(path)
    config.read(paths)

    return config


def load_environment_variables(config):
    db_config = config['db']
    if 'IREKUA_DATABASE_HOST' not in os.environ:
        os.environ['IREKUA_DATABASE_HOST'] = db_config.get('host')

    if 'IREKUA_DATABASE_PORT' not in os.environ:
        os.environ['IREKUA_DATABASE_PORT'] = db_config.get('port')

    if 'IREKUA_DATABASE_NAME' not in os.environ:
        os.environ['IREKUA_DATABASE_NAME'] = db_config.get('name')

    if 'IREKUA_DATABASE_USER' not in os.environ:
        os.environ['IREKUA_DATABASE_USER'] = db_config.get('user')

    if 'IREKUA_DATABASE_PASSWORD' not in os.environ:
        os.environ['IREKUA_DATABASE_PASSWORD'] = db_config.get('password')


def check_app_name(name, repository_info):
    if name not in repository_info:
        message = (
            'Error: Invalid value for "name": invalid choice: {name}.\n'
            'Choose from: {list}')

        name_list = '\n'.join(['\t[-] {}'.format(name) for name in repository_info])
        message = message.format(name=name, list=name_list)

        raise click.BadParameter(message, param='name', param_hint='name')
