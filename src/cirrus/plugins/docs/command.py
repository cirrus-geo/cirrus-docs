import click


from cirrus.cli.utils import click as utils_click


from . import constants


@click.group(
    help=constants.DESC,
    cls=utils_click.AliasedShortMatchGroup,
)
def docs():
    pass


@docs.command()
@utils_click.requires_project
def compile(project):
    '''
    Compile all documentation source into docs build directory.
    '''
    from .import compiler
    compiler.compile_project_docs(project)


@docs.command()
@utils_click.requires_project
@click.argument(
    'name',
    metavar='name',
)
def init(project, name):
    '''
    Initialize project documentation with default configuration.
    '''
    from . import templater
    templater.make_docs(project, name)
