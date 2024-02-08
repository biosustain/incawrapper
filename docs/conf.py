# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parents[1].resolve()
sys.path.insert(0, str(Path("..").resolve()))

# -- Project information -----------------------------------------------------

project = "incawrapper"
copyright = "2021, Biosustain"
author = "Biosustain"

# The full version, including alpha/beta/rc tags
release = "0.0.1"


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "numpydoc",
    "nbsphinx",
    #"autoapi.extension",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
autosummary_generate = True
numpydoc_show_class_members = False

# Document Python Code
autoapi_dirs = [ROOT_DIR / "incawrapper"]
autoapi_add_toctree_entry = True

# Enable typehints
autodoc_typehints = "signature"

# -- Options for HTML output -------------------------------------------------

html_title = "incawrapper"
html_theme = "sphinx_material"
html_theme_options = {
    "repo_url": "https://github.com/biosustain/incawrapper",
    "repo_name": "incawrapper",
    "color_primary": "indigo",
    "color_accent": "pink",
    "globaltoc_depth": 3,
}
html_sidebars = {"**": ["globaltoc.html", "localtoc.html"]}
html_collapsible_definitions = True
