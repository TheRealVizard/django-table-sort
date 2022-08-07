import os
import sys
from datetime import datetime

import django

sys.path.insert(0, os.path.abspath(".."))

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"


django.setup()

from __future__ import annotations

project = "django-table-sort"
author = "Eduardo Leyva"
copyright = f"{datetime.now().year}, {author}"

version = "0.2.7"


extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

intersphinx_disabled_domains = ["std"]

html_theme = "sphinx_rtd_theme"
