import shlex

from sphinx.cmd import build

from cirrus.core.project import Project

from . import utils

def doc_dirs_from_project(project: Project):
    docs = project.path.joinpath('docs')
    _src = docs.joinpath('_src')
    _build = docs.joinpath('_build')
    return docs, _src, _build

def build_html(project: Project):
    _, _src, _build = utils.doc_dirs_from_project(project)
    build.main(shlex.split(f'-M html {_src} {_build}'))


def clean(project: Project):
    import shutil
    _, _src, _build = utils.doc_dirs_from_project(project)
    shutil.rmtree(_src)
    shutil.rmtree(_build)
