# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add source directory to path for autodoc
sys.path.insert(0, os.path.abspath("../src"))

# Import version from package
from claude_knowledge_catalyst import __version__

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Claude Knowledge Catalyst"
copyright = "2024-2025, driller"
author = "driller"
release = __version__
version = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.mermaid",
    "sphinx_design",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# RTD environment detection
on_rtd = os.environ.get("READTHEDOCS", None) == "True"

# Theme configuration
html_theme = "furo"
# html_static_path = ['_static']

# RTD-specific configuration
if on_rtd:
    html_context = {
        "display_github": True,
        "github_user": "drillan",
        "github_repo": "claude-knowledge-catalyst",
        "github_version": "main/docs/",
    }

# MyST Parser configuration
myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

# MyST additional configuration
myst_heading_anchors = 3
myst_fence_as_directive = ["mermaid"]

# Furo theme configuration
html_theme_options = {
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#336790",
        "color-brand-content": "#336790",
    },
    "dark_css_variables": {
        "color-brand-primary": "#E5B62F",
        "color-brand-content": "#E5B62F",
    },
}

html_title = "Claude Knowledge Catalyst Documentation"
html_short_title = "CKC Docs"

# SEO and metadata
html_meta = {
    "description": "Claude Knowledge Catalyst - 知識の触媒作用を実現する統合的な知識管理システム",
    "keywords": "Claude, Automation, Knowledge Management, Obsidian, Documentation, Python",
    "author": "driller",
    "viewport": "width=device-width, initial-scale=1.0",
}

# Favicon and logo
html_favicon = "_static/favicon.ico"

# Additional HTML options
html_use_index = True
html_split_index = False
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True

# Autodoc configuration
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "show-inheritance": True,
}

# Source file suffixes
source_suffix = {
    ".rst": None,
    # '.md': None,
}

# Napoleon configuration
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False

# Intersphinx configuration
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
    "myst": ("https://myst-parser.readthedocs.io/en/latest/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "click": ("https://click.palletsprojects.com/", None),
}

# External links
linkcheck_ignore = [
    r"http://localhost:\d+/",
    r"https://example\.com.*",
]

# Performance optimizations for RTD
nitpicky = False  # Don't fail on missing references
suppress_warnings = ["myst.header"]
