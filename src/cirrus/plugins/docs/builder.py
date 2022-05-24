import shlex

from pathlib import Path
from sphinx.cmd import build


# TODO: support other formats
# TODO: support custom build commands
def build_html(output_dir: Path, staging_dir: Path) -> None:
    build.main(shlex.split(f'-M html {staging_dir} {output_dir}'))
