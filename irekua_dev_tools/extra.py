import click

from irekua_dev_tools.utils import clear_target_directory



@click.command()
@click.pass_context
@click.option('--silent', '-s', is_flag=True)
def clean(ctx, silent):
    target = ctx.obj['target']
    repository_info = ctx.obj['repository_info']

    clear_target_directory(target, repository_info, silent=silent)
