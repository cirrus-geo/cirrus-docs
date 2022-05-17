from importlib import import_module
from pathlib import Path
from pkg_resources import iter_entry_points

from cirrus.docs import src
from cirrus.core.project import Project
from cirrus.core.utils import misc

from . import utils



def make_toctree(toc_items: [str], maxdepth: int=2, caption: str=None) -> str:
    toctree = ['.. toctree::']
    toctree.append(f'   :maxdepth: {maxdepth}')

    if caption:
        toctree.append(f'   :caption: {caption}')

    toctree.append('')

    for item in toc_items:
        toctree.append(f'   {item}')

    return '\n'.join(toctree)


def make_index_section(title: str, toctree: str, desc: str=None, heading_char='-') -> str:
    section = [title]
    section.append(heading_char * len(title))
    section.append('')

    if desc:
        section.append(desc)
        section.append('')

    section.append(toctree)

    return '\n'.join(section)


def generate_index(
    has_project: bool=True,
    has_cirrus: bool=True,
    has_plugins: bool=True,
    has_components: bool=True,
):
    index = '''|project_name| pipeline documentation
=====================================

Welcome to the docs for |project_name|!


'''

    if has_project:
        index += make_index_section(
            'Project documentation',
            make_toctree(['project/index']),
        )
        index += '\n'*3

    if has_cirrus:
        index += make_index_section(
            'Cirrus documentation',
            make_toctree(['cirrus/index']),
        )
        index += '\n'*3

    if has_plugins:
        index += make_index_section(
            'Plugin documentation',
            make_toctree(['plugins/index']),
        )
        index += '\n'*3

    if has_components:
        index += make_index_section(
            'Component READMEs',
            make_toctree(['components/index']),
            desc='Documentation for components built-in, from plugins, and from the project.',
        )
        index += '\n'*3

    index += '''Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
'''

    return index


def placeholder(name: str, text: str, heading_char: str='='):
    content = [name]
    content.append(heading_char * len(name))
    content.append('')
    content.append(text)
    return '\n'.join(content)


def compile_project_docs(project: Project):
    docs = project.path.joinpath('docs')
    _src = utils.make_dir(docs, '_src')

    # link conf.py into _src
    utils.make_link(_src, 'conf.py', docs.joinpath('conf.py'))

    # cirrus docs
    utils.make_link(_src, 'cirrus', Path(src.__file__).parent)

    # project docs
    utils.make_link(_src, 'project', misc.relative_to(_src, docs.joinpath('src')))

    # plugin docs
    plugin_indices = []
    plugins = utils.make_dir(_src, 'plugins')
    for plugin in iter_entry_points('cirrus.plugins'):
        try:
            plugin_docs = import_module(plugin.module_name + '.docs.src')
        except ImportError as e:
            plugin_dir = utils.make_dir(plugins, plugin.name)
            utils.make_file(plugin_dir, 'index.rst', text=placeholder(
                plugin.name,
                'Plugin is either missing documentation or docs are misconfigured.',
            ))
        else:
            utils.make_link(
                plugins,
                plugin.name,
                Path(plugin_docs.__file__).parent,
                force=True,
            )

        plugin_indices.append(f'{plugin.name}/index')

    utils.make_file(
        plugins,
        'index.rst',
        text=make_index_section(
            'Installed plugins',
            make_toctree(plugin_indices),
        ),
        overwrite=True,
    )

    # pull in component READMEs
    comp_indices = []
    comp_dir = utils.make_dir(_src, 'components')
    for group in project.groups:
        if not hasattr(group, 'readme'):
            continue

        group_dir = utils.make_dir(comp_dir, group.group_name)
        comp_indices.append(f'{group.group_name}/index')

        readmes = []
        for component in group:
            name = f'{component.name}.md'
            utils.make_file(
                group_dir,
                name,
                text=(component.readme.content or placeholder(
                    component.name,
                    'This component appears to missing a README.',
                )),
                overwrite=True,
            )
            readmes.append(name)

        utils.make_file(
            group_dir,
            'index.rst',
            text=make_index_section(
                f'Available {group.group_name}',
                make_toctree(readmes),
            ),
            overwrite=True,
        )

    utils.make_file(
        comp_dir,
        'index.rst',
        text=make_index_section(
            'Component READMEs',
            make_toctree(comp_indices),
        ),
        overwrite=True,
    )

    # top-level index
    utils.make_file(
        _src,
        'index.rst',
        text=generate_index(
            has_plugins=bool(plugin_indices),
        ),
        overwrite=True,
    )
