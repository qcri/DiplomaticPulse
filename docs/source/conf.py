"""
 Configuration file for the Sphinx documentation builder.

 This file only contains a selection of the most common options. For a full
 list see the documentation:
 https://www.sphinx-doc.org/en/master/usage/configuration.html

"""

import os
import sys
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('../../'))

project = 'Diplomatic Pulse'
copyright = '2022, QCRI'
author = 'QCRI'
release = '0.0.1'
extensions = [
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']

exclude_patterns = []

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']

version = '0.0.1'
