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
def stage(project):
    '''
    Stage all docs sources in preparation for sphinx build.
    '''
    from . import compiler
    compiler.compile_project_docs(project)


@docs.command()
@utils_click.requires_project
def build(project):
    '''
    Build all docs from source into html.
    '''
    from . import compiler
    from . import builder
    compiler.compile_project_docs(project)
    builder.build_html(project)


@docs.command()
@utils_click.requires_project
def clean(project):
    '''
    Remove docs staging and build directories.
    '''
    from . import builder
    builder.clean(project)


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
