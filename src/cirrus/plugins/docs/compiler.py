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


def generate_plugins(_src: Path):
    plugin_indices = compile_plugin_docs(_src)
    if plugin_indices:
        return make_toctree(
            plugin_indices,
            caption='Plugin documentation',
            glob=True,
            maxdepth=1,
            titles_only=True,
        )


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


def generate_components(_src: Path, project: Project):
    component_indices = compile_component_readmes(_src, project)
    if component_indices:
        return make_toctree(
            ['components/*/index'],
            caption='Component READMEs',
            maxdepth=2,
            glob=True,
            titles_only=True,
        )


def link_cirrus_geo_docs(_src: Path):
    try:
        import cirrus.docs.src as src
    except ImportError:
        return None
    return utils.make_link(_src, 'cirrus', Path(src.__file__).parent)


def generate_cirrus_geo(_src: Path):
    if link_cirrus_geo_docs(_src):
        return make_toctree(
            ['cirrus/index'],
            caption='Cirrus documentation',
        )


def link_cirrus_lib_docs(_src: Path):
    try:
        import cirrus.lib.docs.src as src
    except ImportError:
        return None
    return utils.make_link(_src, 'cirrus-lib', Path(src.__file__).parent)


def generate_cirrus_lib(_src: Path):
    if link_cirrus_lib_docs(_src):
        return make_toctree(
            ['cirrus-lib/index'],
            caption='Cirrus-lib documentation',
        )


def link_project_docs(_src: Path, docs: Path):
    src = docs.joinpath('src')
    if not src.is_dir():
        return None
    return utils.make_link(_src, 'project', misc.relative_to(_src, src))


def generate_project(_src: Path, docs: Path):
    if link_project_docs(_src, docs):
        return make_toctree(
            ['project/index'],
            caption='Project documentation',
        )


def compile_project_docs(project: Project):
    docs, _src, _ = utils.doc_dirs_from_project(project)
    _src.mkdir(exist_ok=True)
    utils.make_link(_src, 'conf.py', docs.joinpath('conf.py'))

    index_sections = ['Welcome to the docs for |project_name|!']
    index_sections.append(generate_project(_src, docs))
    index_sections.append(generate_cirrus_geo(_src))
    index_sections.append(generate_cirrus_lib(_src))
    index_sections.append(generate_plugins(_src))
    index_sections.append(generate_components(_src, project))

    utils.make_file(
        _src,
        'index.rst',
        text=make_section(
            '|project_name| pipeline documentation',
            [ele for ele in index_sections if ele],
            1,
        ),
        overwrite=True,
    )
