===============
Getting started
===============

The test models
===============

For example purposes, we'll use a simplified book app. Here is our models.

.. code-block:: python

    # app/models.py


    class Person(models.Model):
        name = models.CharField(max_length=100, verbose_name="First Name")
        age = models.IntegerField(verbose_name="Age in Years")

        def __str__(self):
            return self.name

Creating django-table-sort Table
===============================

.. code-block:: python

    from django.shortcuts import render
    from django_table_sort.table import TableSort

    from app.models import Person


    def view(request):
        table = TableSort(request, Person.objects.all())
        return render(request, "template.html", context={"table": table})
