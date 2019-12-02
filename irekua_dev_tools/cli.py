import click

from irekua_dev_tools.utils import load_config
from irekua_dev_tools.utils import get_working_directory
from irekua_dev_tools.utils import load_environment_variables
from irekua_dev_tools.utils import load_repository_info

from . import git
from . import dev
from . import config
from . import db

from .extra import clean


@click.group()
@click.pass_context
@click.option('--config-file', '-c', 'config_file', type=click.Path())
@click.option('--target', '-t', type=click.Path(exists=True))
@click.option('--default-config', '-dc', 'default_config', is_flag=True)
def cli(ctx, config_file, target, default_config):
    config = load_config(path=config_file, aux_config=not default_config)
    repository_info = load_repository_info(config)
    load_environment_variables(config)

    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['repository_info'] = repository_info

    if target is None:
        target = get_working_directory(ctx.obj['config'])
    ctx.obj['target'] = target


cli.add_command(dev.cli)
cli.add_command(git.cli)
cli.add_command(config.cli)
cli.add_command(db.cli)
cli.add_command(clean)
