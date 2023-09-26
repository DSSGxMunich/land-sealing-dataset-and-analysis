# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.append(os.path.abspath('../../src'))
sys.path.append(os.path.abspath('../../'))

# -- Project information -----------------------------------------------------

project = 'DSSGx Munich'
copyright = '2023, DSSGx Munich Fellows'
author = 'DSSGx Munich Fellows'

# The full version, including alpha/beta/rc tags
release = '2023'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc',
              'sphinx.ext.mathjax',  # for math equations
              'sphinx.ext.autosummary',  # for automatic docstrings
              'sphinx.ext.intersphinx',
              'sphinx.ext.napoleon',  # for google style docstrings
              'sphinx.ext.githubpages',  # for github pages
              'sphinx.ext.duration',
              'sphinx.ext.doctest',
              "nbsphinx",  # for jupyter notebooks
              "sphinx_gallery.load_style",  # for jupyter notebooks as gallery
              ]

nbsphinx_thumbnails = {
    'content/notebooks/*': '_static/dssgx_main.png',
}
# nbsphinx_thumbnails = {
#     'content/notebooks/*': 'assets/dssgx_main.png',
#     'orphan': 'assets/dssgx_main.png',
# }

source_suffix = [".rst", ".md"]
napoleon_google_docstring = True
napoleon_use_param = False
napoleon_use_ivar = True
add_module_names = False
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_logo = "assets/dssgx_main.png"
html_theme_options = {
    "logo_only": True,
    "display_version": True,
    "style_nav_header_background": "white",
    "collapse_navigation": False,
    "analytics_anonymize_ip": True,
}
html_js_files = ["js/redirect.js"]
html_css_files = [
    "css/custom.css",
]
