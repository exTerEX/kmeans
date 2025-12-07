"""Sphinx configuration for kmeans documentation."""

import os
import sys
import re
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath('../src'))

def get_version():
    """Extract version from __init__.py"""
    init_file = os.path.join(os.path.dirname(__file__), "../src/kmeans/__init__.py")
    with open(init_file, "r") as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)


# Mock the C extension module to avoid import errors during doc build
class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name): # type: ignore
        return MagicMock()

MOCK_MODULES = ['kmeans._kmeans']
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

# Project information
project = 'kmeans'
copyright = '2024, Andreas Sagen'
author = 'Andreas Sagen'
release = get_version()

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
    'myst_parser',  # For Markdown support
]

# Remove breathe for now since we don't have Doxygen XML
# 'breathe',

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Napoleon settings for Google/NumPy docstring style
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
}
autodoc_mock_imports = ['numpy', '_kmeans']

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}

# HTML output options
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
}

# MyST parser settings
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

# Suppress warnings about missing references
nitpicky = False
