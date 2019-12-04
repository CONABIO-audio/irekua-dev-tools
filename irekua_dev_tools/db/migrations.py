import click

from irekua_dev_tools.dev.install import run_manage


def get_migration_order(repository_info):
    apps_with_migrations = [
        name for name in repository_info
        if repository_info[name].get('has_migrations', False)
    ]

    dependencies = {
        name: [
            dependency for dependency in repository_info[name]['dependencies']
            if dependency in apps_with_migrations]
        for name in apps_with_migrations
    }

    ordered_list = []

    while True:
        no_dependency_list = [
            name for name in dependencies
            if len(dependencies[name]) == 0]
        ordered_list += no_dependency_list

        updated_dependencies = {
            name: [
                dependency for dependency in dependencies[name]
                if dependency not in no_dependency_list]
            for name in dependencies if name not in no_dependency_list}

        if len(updated_dependencies) == 0:
            break

        dependencies = updated_dependencies

    return ordered_list


def migrate_app(name, target, venvs_dir=None):
    message = '[+] Making migrations for app: {}'.format(name)
    click.secho(message, fg='green')

    try:
        run_manage(target, name, 'migrate', None, venvs_dir=venvs_dir)
    except click.ClickException as error:
        raise error
    except RuntimeError as error:
        message = (
            'Error with database connection.\n'
            'Run irekua db check for diagnostics').format(error=str(error))
        raise click.ClickException(message)



def migrate_database(repository_info, target, venvs_dir=None):
    ordered_migration_apps = get_migration_order(repository_info)

    for app in ordered_migration_apps:
        if has_pending_migrations(app, target, venvs_dir=venvs_dir):
            migrate_app(app, target, venvs_dir=venvs_dir)


def has_pending_migrations(name, target, venvs_dir=None):
    try:
        app_name = name.lower().replace('-', '_')
        output = run_manage(
            target,
            name,
            'migrate',
            ['--plan', '--fake'],
            venvs_dir=venvs_dir,
            stdout=False,
            stderr=False)

        if output.returncode != 0:
            print(output.stdout)
            raise RuntimeError

        stdout = output.stdout.decode('utf-8')
        return 'No planned migration operations' not in stdout

    except click.ClickException as error:
        raise error
    except RuntimeError as error:
        message = (
            'Error with database connection.\n'
            'Run irekua db check for diagnostics').format(error=str(error))
        raise click.ClickException(message)


def check_migration_status(repository_info, target, venvs_dir=None):
    ordered_migration_apps = get_migration_order(repository_info)

    migrations_complete = True
    for app in ordered_migration_apps:
        try:
            if has_pending_migrations(app, target, venvs_dir=venvs_dir):
                message = '[-] Missing migrations for app {}'.format(app)
                click.secho(message, fg='yellow')

                migrations_complete = False
        except:
            message = (
                '[-] Missing migrations for uninstalled app {name}. '
                'Please run (irekua dev install {name}) and then '
                '(irekua db migrate)'.format(name=app))
            click.secho(message, fg='red')

            migrations_complete = False

    return migrations_complete
