# Django-table-sort

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/TheRealVizard/django-table-sort/main.svg)](https://results.pre-commit.ci/latest/github/TheRealVizard/django-table-sort/main) [![Documentation Status](https://readthedocs.org/projects/django-table-sort/badge/?version=latest)](https://django-table-sort.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/TheRealVizard/django-table-sort/branch/main/graph/badge.svg?token=KGXHPZ6HOB)](https://codecov.io/gh/TheRealVizard/django-table-sort) ![django-table-sort](https://img.shields.io/pypi/v/django-table-sort?color=blue) ![python-versions](https://img.shields.io/pypi/pyversions/django-table-sort) ![django-versions](https://img.shields.io/pypi/frameworkversions/django/django-table-sort?label=django) ![license](https://img.shields.io/pypi/l/django-table-sort?color=blue) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![downloads](https://img.shields.io/pypi/dm/django-table-sort)

Create tables with sorting links on the headers in Django templates.

This is currently [WIP](https://en.wikipedia.org/wiki/Work_in_process), so many other features will come in future releases.
## Installation

**First**, install with pip:

```bash
pip install django-table-sort
```

**Second**, add the app to your INSTALLED_APPS setting:

```python
INSTALLED_APPS = [
    ...,
    "django_table_sort",
    ...,
]
```

## Usage
**First**, add the static to your Template:

```html
<link rel="stylesheet" href="{% static 'django_table_sort.css' %}"/>
```

`django-sort-table` uses by default Font Awesome 6 to display the icons, so you might need to add it too.

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.2/css/all.min.css" integrity="sha512-1sCRPdkRXhBV2PBLUdRb4tMg1w2YPf37qatUFeS7zlBy7jJI8Lf4VHwWfZZfpXtYSLy85pkm9GaYVYMfw5BC1A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
```

**Second**, Use `django-table-sort` to display your tables.

In your _view.py_ file:

```python
class ListViewExample(ListView):
    model = Person
    template_name: str = "base.html"
    ordering_key = "o"

    def get_ordering(self) -> tuple:
        return self.request.GET.getlist(
            self.ordering_key, None
        )  # To make Django use the order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table"] = TableSort(
            self.request,
            self.object_list,
            sort_key_name=self.ordering_key,
            table_css_clases="table table-light table-striped table-sm",
        )
        return context
```

In your _template.html_ file:

```html
{{ table.render }}
```

Result:

The table is render with 2 link, one to Toggle the sort direction and another to remove the sort.

<p align="center">
    <img width="375" height="149" src=".\result.png">
</p>

You can filter by each field you declare as a column.
<p align="center">
    <img width="375" height="45" src=".\url_result.png">
</p>
