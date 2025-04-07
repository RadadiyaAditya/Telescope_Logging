# Configuration file for the Sphinx documentation builder.

import os
import sys
import django

sys.path.insert(0, os.path.abspath('../..'))  # path to your project root
os.environ['DJANGO_SETTINGS_MODULE'] = 'telescope_log.settings'
django.setup()


# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Telescope Logging'
copyright = '2025, Aditya Radadiya'
author = 'Aditya Radadiya'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",        # For Google/NumPy style docstrings
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    # "sphinxcontrib.django",       # Optional: better Django support
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
