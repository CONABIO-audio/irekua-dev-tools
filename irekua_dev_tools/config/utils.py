import os
import io
import shutil
import configparser

import click
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

from irekua_dev_tools.utils import load_config
from irekua_dev_tools import BASE_DIR


def print_config(config):
    with io.StringIO() as string_file:
        config.write(string_file)
        config_string = string_file.getvalue()

    lexer = get_lexer_by_name("ini", stripall=True)
    formatter = TerminalFormatter(linenos=False)
    result = highlight(config_string, lexer, formatter)

    click.echo(result)


def backup_config():
    backup_path = os.path.join(BASE_DIR, 'settings.bkp.ini')
    original_path = os.path.join(BASE_DIR, 'settings.ini')

    if not os.path.exists(backup_path):
        shutil.copyfile(original_path, backup_path)
        click.secho('Config file backup created', fg='cyan')



def restore_config():
    backup_path = os.path.join(BASE_DIR, 'settings.bkp.ini')
    original_path = os.path.join(BASE_DIR, 'settings.ini')

    if os.path.exists(backup_path):
        shutil.copyfile(backup_path, original_path)
        click.secho('Configurations restored', fg="green")
        return

    click.secho('No config backup was found.', fg="yellow")


def update_config(
        working_directory=None,
        config_file=None,
        origin=None,
        branch=None):

    config = load_config(path=None, aux_config=False)

    if working_directory:
        config['irekua']['working_directory'] = working_directory

    if config_file:
        config['irekua']['config_file'] = config_file

    if origin:
        config['git']['origin'] = origin

    if branch:
        config['git']['branch'] = branch

    path = os.path.join(BASE_DIR, 'settings.ini')
    with open(path, 'w') as config_file:
        config.write(config_file)

    click.secho('Configuration settings updated', fg='green')


