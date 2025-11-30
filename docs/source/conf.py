# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Pigal-Flask'
copyright = '2025, Malcom Chumchoua Penda'
author = 'Malcom Chumchoua Penda'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


import os
import sys

src_path = os.path.abspath('../..')
print('\n', src_path)
sys.path.insert(0, src_path)
if src_path not in sys.path:
    sys.path.append(src_path)


extensions = [
    'sphinx.ext.todo', 
    'sphinx.ext.autodoc',
    'pallets_sphinx_themes', 
    ]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'flask'
html_static_path = ['_static']
