import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

project = "django-table-sort"
author = "Eduardo Leyva"
copyright = f"{datetime.now().year}, {author}"

version = "0.2.7"


extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon,",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

intersphinx_disabled_domains = ["std"]

html_theme = "sphinx_rtd_theme"
