import shlex
import pytest

from click.testing import CliRunner

from cirrus.plugins.docs.commands import docs


@pytest.fixture(scope='session')
def cli_runner():
    return CliRunner(mix_stderr=False)


@pytest.fixture(scope='session')
def invoke(cli_runner):
    def _invoke(cmd, **kwargs):
        return cli_runner.invoke(docs, shlex.split(cmd), **kwargs)
    return _invoke


def test_nothing(invoke):
    result = invoke('')
    print(result.stdout, result.stderr)
    assert result.exit_code == 0
