from pathlib import Path

from cirrus.core.project import Project

from . import utils


gitignore = '''_build
_src
_conf
'''

conf = '''# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# inherit defaults from base cirrus config
from cirrus.docs.conf import *


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = '{project_name}'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions += []

# Add any paths that contain templates here, relative to this directory.
templates_path += []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns += []

# allow substituting the project name in documents
rst_epilog = f'.. |project_name| replace:: {{project}}'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path += ['_static']

# A list of paths that contain extra files not directly related to the
# documentation, such as robots.txt or .htaccess. Relative paths are taken as
# relative to the configuration directory. They are copied to the output
# directory. They will overwrite any existing file of the same name.
html_extra_path += ['_extra']
'''.format

index = '''
Welcome to the |project_name| pipeline documentation!
=====================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
'''


def make_extra(src: Path):
    extra = utils.make_dir(src, '_extra')
    utils.make_file(extra, '.gitkeep')


def make_static(src: Path):
    static = utils.make_dir(src, '_static')
    utils.make_file(static, '.gitkeep')


def make_src(docs: Path):
    src = utils.make_dir(docs, 'src')
    make_extra(src)
    make_static(src)
    utils.make_file(src, 'index.rst', text=index)


def make_docs(project: Project, project_name: str):
    docs = utils.make_dir(project.path, 'docs')
    make_src(docs)
    utils.make_file(docs, '.gitignore', text=gitignore)
    utils.make_file(docs, 'conf.py', text=conf(project_name=project_name))
