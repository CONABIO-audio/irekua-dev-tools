import os
import shutil
import configparser

import click
from irekua_dev_tools import BASE_DIR
from irekua_dev_tools.repositories import REPOSITORY_INFO


BASE_PATH = os.path.join(BASE_DIR, 'settings.ini')


def clear_target_directory(target, silent=False):
    for name in REPOSITORY_INFO.keys():
        dir_path = os.path.join(target, name)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            message = (
                'Directory for {} succesfully removed ({})'.format(
                    name, dir_path))
            click.secho(message, fg='green')


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
