# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

sys.path.insert(0, str(Path("..").resolve()))

# -- Project information -----------------------------------------------------

project = 'BFAIR'
copyright = '2021, AutoFlowResearch'
author = 'AutoFlowResearch'

# The full version, including alpha/beta/rc tags
release = '0.0.1'


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "numpydoc",
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
autosummary_generate = True
numpydoc_show_class_members = False

# -- Options for HTML output -------------------------------------------------

html_title = "BFAIR"
html_theme = 'sphinx_material'
html_theme_options = {
    "repo_url": "https://github.com/AutoFlowResearch/BFAIR",
    "repo_name": "BFAIR",
    "color_primary": "indigo",
    "color_accent": "pink",
    "globaltoc_depth": 3
}
html_sidebars = {
    "**": ["globaltoc.html", "localtoc.html"]
}
html_static_path = ['_static']
# html_css_files = ["style.css"]
html_collapsible_definitions = True
