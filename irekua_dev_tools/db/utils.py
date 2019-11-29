import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import DuplicateObject

import click


def connect_to_db(db_config, exit=True):
    host = db_config['host']
    user = db_config['user']
    port = db_config['port']
    password = db_config['password']

    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port)
    except psycopg2.OperationalError as error:
        if exit:
            message = (
                'Database error: {}\nPlease make sure postgres is installed and running.\n'
                'Check the current database configuration with the command:  irekua config '
                'show\nTo set a different configuration run:  irekua config set '
                '--help'.format(str(error).strip()))
            click.secho(message, fg='red')
            sys.exit()
        raise error

    return connection


def connect_to_irekua(db_config, exit=True):
    host = db_config['host']
    user = db_config['user']
    name = db_config['name']
    port = db_config['port']
    password = db_config['password']

    try:
        connection = psycopg2.connect(
            dbname=name,
            user=user,
            password=password,
            host=host,
            port=port)
    except psycopg2.OperationalError as error:
        if exit:
            message = (
                'Database error: {}\nPlease run:  irekua db '
                'setup'.format(str(error).strip()))
            click.secho(message, fg='red')
            sys.exit()
        raise error

    return connection


def check_database(db_config):
    connect_to_db(db_config)
    connect_to_irekua(db_config)
    message = 'Database seems ok'
    click.secho(message, fg='green')


def create_database(db_config):
    connection = connect_to_db(db_config)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    name = db_config['name']
    command = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(name))
    cursor.execute(command)
    connection.close()
    message = 'Database created sucessfully'
    click.secho(message, fg='green')


def delete_database(db_config):
    connection = connect_to_db(db_config)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    name = db_config['name']
    command = sql.SQL("DROP DATABASE {}").format(sql.Identifier(name))
    cursor.execute(command)
    connection.close()
    message = 'Database deleted'
    click.secho(message, fg='red')


def configure_database(db_config):
    connection = connect_to_irekua(db_config)
    cursor = connection.cursor()

    try:
        cursor.execute('CREATE EXTENSION postgis;')
        connection.commit()
    except DuplicateObject:
        pass

    connection.close()
    message = 'Database configured sucessfully'
    click.secho(message, fg='green')


def database_exists(db_config):
    try:
        connect_to_irekua(db_config, exit=False)
        return True
    except psycopg2.OperationalError:
        return False


def setup_database(db_config, force=False):
    if force:
        delete_database(db_config)

    if not database_exists(db_config):
        create_database(db_config)

    configure_database(db_config)
