Installation
============

1. Install the package
^^^^^^^^^^^^^^^^^^^^^^

You can install *django-table-sort* via pip_ from PyPI_:

.. code:: console

   $ pip install django-table-sort

2. Add *django-table-sort* to your ``INSTALLED_APPS``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   INSTALLED_APPS = [
       # ...,
       "django_table_sort",
       # ...,
   ]

3. Add the ``CSS`` file to your templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: html

   <! -- Font Awesome 6 for the table icons -->
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.2/css/all.min.css" integrity="sha512-1sCRPdkRXhBV2PBLUdRb4tMg1w2YPf37qatUFeS7zlBy7jJI8Lf4VHwWfZZfpXtYSLy85pkm9GaYVYMfw5BC1A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
   <! -- css to use the header sort icons -->
   <link rel="stylesheet" href="{% static 'django_table_sort.css' %}"/>

Requirements
------------

* Python 3.7+
* Django 3.0+


.. _PyPI: https://pypi.org/
.. _pip: https://pip.pypa.io/
