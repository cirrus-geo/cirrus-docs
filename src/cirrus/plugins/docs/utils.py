import shutil
import click

from pathlib import Path
from click_option_group import OptionGroup

from cirrus.core.project import Project


class OptionProjectDefault(click.Option):
    def get_default(self, ctx, call=False):
        # we always want to resolve a value, for help messages,
        # so we ignore the call parameter's value entirely
        return self.type_cast_value(ctx, self.default(ctx.obj))


def docs_from_project(project: Project):
    return project.path.joinpath('docs') if project.path else None


def output_dir_from_project(project: Project):
    docs = docs_from_project(project)
    return docs.joinpath('_build') if docs else None


def staging_dir_from_project(project: Project):
    docs = docs_from_project(project)
    return docs.joinpath('_src') if docs else None


def project_src_dir_from_project(project: Project):
    docs = docs_from_project(project)
    return docs.joinpath('src') if docs else None


def conf_file_from_project(project: Project):
    docs = docs_from_project(project)
    return docs.joinpath('conf.py') if docs else None


def output_dir(func):
    return click.option(
        '-o',
        '--output-dir',
        cls=OptionProjectDefault,
        default=output_dir_from_project,
        type=click.Path(file_okay=False, resolve_path=True, path_type=Path),
        help='Path to docs build output directory',
        show_default=True,
    )(func)


def staging_dir(func):
    return click.option(
        '-s',
        '--staging-dir',
        cls=OptionProjectDefault,
        default=staging_dir_from_project,
        type=click.Path(file_okay=False, resolve_path=True, path_type=Path),
        help='Path to docs staging directory (to assemble all sources pre-build)',
        show_default=True,
        required=True,
    )(func)


def conf_file(func):
    return click.option(
        '-c',
        '--conf-file',
        cls=OptionProjectDefault,
        default=conf_file_from_project,
        type=click.Path(exists=True, resolve_path=True, readable=True, dir_okay=False, path_type=Path),
        help='Path to sphinx conf.py file to use for docs build',
        show_default=True,
        required=True,
    )(func)


def is_project_src_required(ctx, self, value):
    if not value and ctx.params.get('include_project_docs', False):
        raise click.BadParameter(
            'Must provide project docs source directory if project docs included',
        )


def project_src_dir(func):
    return click.option(
        '-p',
        '--project-src-dir',
        cls=OptionProjectDefault,
        default=project_src_dir_from_project,
        type=click.Path(
            exists=True,
            resolve_path=True,
            readable=True,
            file_okay=False,
            path_type=Path,
        ),
        help='Path to project docs source directoy (for project-specific documentation)',
        show_default=True,
        callback=is_project_src_required,
    )(func)


def default_include(ctx, self, value):
    group_opts = set(self.group.get_options(ctx))

    # This is a callback called _during_ arg parsing, therefore we can't set
    # defaults until parsing the last of the params. If we have more than one
    # param remaining we simply return.
    if len(group_opts.difference(group_opts.intersection(set(ctx.params)))) > 1:
        return value

    # Otherwise, we are processing the last of the group options and we need to
    # calculate and set the default value for unspecified group parameters.
    #
    # The `get` here handles the one last param we are processing and thus we
    # can use the `value` for its value.
    opts = {opt: ctx.params.get(opt, value) for opt in group_opts}
    specified_opts = {opt: val for opt, val in opts.items() if val is not None}

    # if all specified are included, those missing are excluded
    # if all specified are excluded, those missing are included
    # if those specified are mixed, those missing are included
    # if none are specified, all are included
    default = True
    if specified_opts and all(specified_opts.values()):
        default = False

    for opt, val in opts.items():
        if val is None:
            ctx.params[opt] = default

    return value if value is not None else default


def doc_includes(func):
    group = OptionGroup(
        'Include options',
        help=(
            'Flags to control what is included into built docs. '
            'All sections are included (if available) by default. '
            'If any are explicitly excluded, the remainder are implicitly included. '
            'If any are explicitly included and none are explicitly excluded, '
            'the remainder are implcitly excluded.'
        ),
    )
    return group.option(
        '--include-project-docs/--exclude-project-docs',
        default=None,
        help='Stage/unstage project documentation',
        callback=default_include,
    )(group.option(
        '--include-core-docs/--exclude-core-docs',
        default=None,
        help='Stage/unstage cirrus-geo documentation',
        callback=default_include,
    )(group.option(
        '--include-lib-docs/--exclude-lib-docs',
        default=None,
        help='Stage/unstage cirrus-lib documentation',
        callback=default_include,
    )(group.option(
        '--include-plugin-docs/--exclude-plugin-docs',
        default=None,
        help='Stage/unstage plugin documentation',
        callback=default_include,
    )(group.option(
        '--include-component-docs/--exclude-component-docs',
        default=None,
        help='Stage/unstage component documentation',
        callback=default_include,
    )(func)))))


def make_dir(parent: Path, name: str) -> Path:
    path = parent.joinpath(name)
    path.mkdir(exist_ok=True)
    return path


def make_file(
    parent: Path,
    name: str,
    text: str=None,
    mode: int=438,
    overwrite: bool=False,
) -> Path:
    path = parent.joinpath(name)
    exists = path.is_file()

    if exists and not overwrite:
        return path

    path.touch(mode=mode, exist_ok=True)

    if text:
        path.write_text(text)

    return path


def make_link(parent: Path, name: str, target: Path, force=False) -> Path:
    path = parent.joinpath(name)

    if path.is_symlink() and path.readlink() == target:
        return path
    elif not (force and path.exists()):
        pass
    elif path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif not (path.is_symlink() and path.readlink() == target):
        path.unlink()

    path.symlink_to(target)
    return path
