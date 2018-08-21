#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# LDT documentation build configuration file, created by
# sphinx-quickstart on Thu Feb  1 22:49:56 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
import shutil
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('...'))
from ldt import __version__
sys.path.append(os.path.join(os.path.dirname(__name__), '..'))
# root = os.path.abspath(".")
root = os.path.dirname(os.path.realpath(__file__))
# root = root.rstrip("/")
tutorial_path = os.path.join(root, "Tutorial/resources/.ldt-config.yaml")
root = root.rstrip("/docs/source")
sys.path.insert(0, root)
sample_file = os.path.join(root, "ldt/tests/sample_files/.ldt-config.yaml")
shutil.copyfile(sample_file, tutorial_path)

autodoc_mock_imports = ["nltk", "enchant", "pyenchant"]

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Linguistic Diagnostics Toolkit'
copyright = '2018, LDT team'
author = 'LDT team'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = __version__
# The full version, including alpha/beta/rc tags.
release = __version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# up-to-date values here: https://github.com/bitprophet/alabaster/blob/master/alabaster/theme.conf

html_theme_options = {
"github_button": True,
'github_repo': 'https://github.com/ookimi/ldt',
"description": "<br/> <br/>",
"logo": "ldt_logo.png",
"fixed_sidebar": True,
"sidebar_includehidden": True,
"show_powered_by": False,
"sidebar_collapse": True,
"show_relbars": True,
"font_size": "0.93em",
"code_font_size": "0.85em",
"sidebar_width":  "25em",
"page_width": "90em",
# "show_related": True,
"extra_nav_links": {"Project website":"http://ldtoolkit.space",
                    "Research paper":"http://ldtoolkit.space"}
                    # 'Index': 'genindex.html',
                    # 'Module Index': 'modindex.html'}
}

# html_logo = '/home/anna/PycharmProjects/docs/source/media/wordcloud.png'
# html_logo = '/home/anna/PycharmProjects/docs/source/media/ldt_logo.png'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': ['about.html',
        'localtoc.html',
        # 'sourcelink.html'
        # 'globaltoc.html',
        # 'relations.html',  # needs 'show_related': True theme option to display
        'navigation.html',
        'searchbox.html'
           ],
    "custom": []
}
#todo: add changelog
#todo: installation section separately

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'LDTdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'LDT.tex', 'LDT Documentation',
     'LDT team', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'ldt', 'LDT Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'LDT', 'LDT Documentation',
     author, 'LDT', 'One line description of project.',
     'Miscellaneous'),
]



