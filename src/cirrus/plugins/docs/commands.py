import click

from pathlib import Path
from cirrus.cli.utils import click as utils_click

from . import constants, utils


@click.group(
    help=constants.DESC,
    cls=utils_click.AliasedShortMatchGroup,
)
def docs():
    pass


@docs.command()
@utils_click.pass_project
@utils.staging_dir
@utils.project_src_dir
@utils.conf_file
@click.option(
    '--custom-index-include',
    type=click.Path(dir_okay=False, resolve_path=True, path_type=Path),
    help='Path to a file containing custom content override for root index.rst.',
    default=None,
)
@utils.doc_includes
def stage(
    project,
    staging_dir,
    project_src_dir,
    conf_file,
    custom_index_include,
    include_project_docs,
    include_core_docs,
    include_lib_docs,
    include_plugin_docs,
    include_component_docs,
):
    '''
    Stage all docs sources in preparation for build.
    '''
    from . import compiler
    from cirrus.core.utils.misc import clean_dir

    staging_dir.mkdir(exist_ok=True)
    clean_dir(staging_dir)

    sections = []
    if include_project_docs:
        section = compiler.generate_project(staging_dir, project_src_dir)
        sections.append(section) if section else None
    if include_core_docs:
        section = compiler.generate_cirrus_geo(staging_dir)
        sections.append(section) if section else None
    if include_lib_docs:
        section = compiler.generate_cirrus_lib(staging_dir)
        sections.append(section) if section else None
    if include_plugin_docs:
        section = compiler.generate_plugins(staging_dir)
        sections.append(section) if section else None
    if include_component_docs:
        section = compiler.generate_components(staging_dir, project)
        sections.append(section) if section else None

    compiler.compile(
        conf_file,
        staging_dir,
        sections,
        custom_index_include=custom_index_include,
    )


@docs.command()
@utils.output_dir
@utils.staging_dir
def build(output_dir, staging_dir):
    '''
    Build all docs from staged sources into html.
    '''
    from . import builder
    builder.build_html(output_dir, staging_dir)


@docs.command()
@utils.output_dir
@utils.staging_dir
def clean(output_dir, staging_dir):
    '''
    Remove all files from staging and build directories.
    '''
    # TODO: once clean_dir is in a cirrus release update the
    # required cirrus-geo version and replace the it here with
    # the one imported from cirrus-geo and clean up in utils
    #from cirrus.core.utils.misc import clean_dir
    utils.clean_dir(output_dir)
    utils.clean_dir(staging_dir)


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
