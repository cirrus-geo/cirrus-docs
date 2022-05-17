from importlib import import_module
from pathlib import Path
from pkg_resources import iter_entry_points

from cirrus.core.project import Project
from cirrus.core.utils import misc

from . import utils


HEADING_LEVELS = {
    1: '=',
    2: '-',
    3: '*',
    4: '^',
}


def make_toctree(
    toc_items: [str],
    maxdepth: int=2,
    caption: str=None,
    titles_only: bool=False,
    glob: bool=False,
    hidden: bool=False,
) -> str:
    toctree = ['.. toctree::']
    toctree.append(f'   :maxdepth: {maxdepth}')

    if hidden:
        toctree.append('   :hidden:')

    if glob:
        toctree.append('   :glob:')

    if titles_only:
        toctree.append('   :titlesonly:')

    if caption:
        toctree.append(f'   :caption: {caption}')

    toctree.append('')

    for item in toc_items:
        toctree.append(f'   {item}')

    return '\n'.join(toctree)


def make_section(title: str, subsections: [str], heading: int) -> str:
    heading_char = HEADING_LEVELS[heading]
    return ('\n' * 3).join([f'{title}\n{heading_char * len(title)}'] + subsections)


def compile_plugin_docs(_src: Path):
    plugin_indices = []
    plugins = utils.make_dir(_src, 'plugins')
    for plugin in iter_entry_points('cirrus.plugins'):
        try:
            plugin_docs = import_module(plugin.module_name + '.docs.src')
        except ImportError as e:
            plugin_dir = utils.make_dir(plugins, plugin.name)
            utils.make_file(
                plugin_dir,
                'index.rst',
                text=make_section(
                    plugin.name,
                    ['Plugin is either missing documentation or docs are misconfigured.'],
                    1,
                ),
            )
        else:
            utils.make_link(
                plugins,
                plugin.name,
                Path(plugin_docs.__file__).parent,
                force=True,
            )

        plugin_indices.append(f'{plugin.name} <plugins/{plugin.name}/index>')

    return plugin_indices


def compile_component_readmes(_src: Path, project: Project):
    component_indices = []
    comp_dir = utils.make_dir(_src, 'components')
    for group in project.groups:
        if not hasattr(group, 'readme'):
            continue

        group_dir = utils.make_dir(comp_dir, group.group_name)

        readmes = []
        for component in group:
            name = f'{component.name}.md'
            utils.make_file(
                group_dir,
                name,
                text=(component.readme.content or make_section(
                    component.name,
                    ['This component appears to missing a README.'],
                    1,
                )),
                overwrite=True,
            )
            readmes.append(f'{component.name} <{name}>')

        utils.make_file(
            group_dir,
            'index.rst',
            text=make_section(
                f'{group.group_display_name}',
                [make_toctree(readmes, titles_only=True, glob=True, maxdepth=1)],
                1,
            ),
            overwrite=True,
        )

        component_indices.append(f'{group.group_display_name} <{group.group_name}/index>')

    return component_indices


def link_cirrus_geo_docs(_src: Path):
    import cirrus.docs.src as src
    return utils.make_link(_src, 'cirrus', Path(src.__file__).parent)


def link_cirrus_lib_docs(_src: Path):
    import cirrus.lib.docs.src as src
    return utils.make_link(_src, 'cirrus-lib', Path(src.__file__).parent)


def link_project_docs(_src: Path, docs: Path):
    return utils.make_link(_src, 'project', misc.relative_to(_src, docs.joinpath('src')))


def compile_project_docs(project: Project):
    docs = project.path.joinpath('docs')
    _src = utils.make_dir(docs, '_src')
    # link conf.py into _src
    utils.make_link(_src, 'conf.py', docs.joinpath('conf.py'))
    # cirrus docs
    link_cirrus_geo_docs(_src)
    link_cirrus_lib_docs(_src)
    # project docs
    link_project_docs(_src, docs)
    # plugin docs
    plugin_indices = compile_plugin_docs(_src)
    # pull in component READMEs
    component_indices = compile_component_readmes(_src, project)

    # top-level index
    index_sections = ['Welcome to the docs for |project_name|!']
    index_sections.append(make_toctree(
        ['project/index'],
        caption='Project documentation',
    ))
    index_sections.append(make_toctree(
        ['cirrus/index'],
        caption='Cirrus documentation',
    ))
    index_sections.append(make_toctree(
        ['cirrus-lib/index'],
        caption='Cirrus-lib documentation',
    ))
    if plugin_indices:
        index_sections.append(make_toctree(
            plugin_indices,
            caption='Plugin documentation',
            glob=True,
            maxdepth=1,
            titles_only=True,
        ))
    if component_indices:
        index_sections.append(make_toctree(
            ['components/*/index'],
            caption='Component READMEs',
            maxdepth=2,
            glob=True,
            titles_only=True,
        ))
    utils.make_file(
        _src,
        'index.rst',
        text=make_section(
            '|project_name| pipeline documentation',
            index_sections,
            1,
        ),
        overwrite=True,
    )
