[![build-status-image]][build-status]
[![coverage-status-image]][codecov]
[![pypi-version]][pypi]

**This repo has been archived and is no longer maintained.**

# cirrus-docs

cirrus-docs is a plugin for the [cirrus-geo] processing pipeline framework to
add documentation commands to the `cirrus` cli. The plugin allows a cirrus
project instance to develop and build documentation, pulling in the docs for
cirrus-geo, cirrus-lib, all of the available components, and any installed
plugins.

## Quickstart

cirrus-docs in `pip`-installable:

```
pip install cirrus-docs
```

When installed alongside [cirrus-geo], it will add a `docs` subcommand to the `cirrus` cli, which can be used within a Cirrus project to initialize, stage, and build the project documentation:

```
~ ❯ cd project-dir
~/project-dir ❯ cirrus docs init
~/project-dir ❯ cirrus docs stage
`/project-dir ❯ cirrus docs build
```

cirrus-docs is built on top of [sphinx]. See the [full plugin
documentation][docs] for more information about how to use it.

[sphinx]: https://www.sphinx-doc.org/en/master/
[docs]: https://cirrus-geo.github.io/cirrus-docs/
[cirrus-geo]: https://github.com/cirrus-geo/cirrus-geo
[build-status-image]: https://github.com/cirrus-geo/cirrus-docs/actions/workflows/python-test.yml/badge.svg
[build-status]: https://github.com/cirrus-geo/cirrus-docs/actions/workflows/python-test.yml
[coverage-status-image]: https://img.shields.io/codecov/c/github/cirrus-geo/cirrus-docs/master.svg
[codecov]: https://codecov.io/github/cirrus-geo/cirrus-docs?branch=master
[pypi-version]: https://img.shields.io/pypi/v/cirrus-docs.svg
[pypi]: https://pypi.org/project/cirrus-docs/
