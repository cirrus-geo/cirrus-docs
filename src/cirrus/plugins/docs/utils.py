import shutil

from pathlib import Path


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
