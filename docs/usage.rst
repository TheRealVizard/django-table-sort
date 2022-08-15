===============
Getting started
===============

The test models
***************

For example purposes, we'll use a simplified book app. Here is our models.

.. code-block:: python

    # app/models.py


    class Person(models.Model):
        name = models.CharField(max_length=100, verbose_name="First Name")
        age = models.IntegerField(verbose_name="Age in Years")

        def __str__(self):
            return self.name

Basic usage
***********

.. code-block:: python

    from django.shortcuts import render
    from django_table_sort.table import TableSort

    from app.models import Person


    def view(request):
        table = TableSort(request, Person.objects.all())
        return render(request, "template.html", context={"table": table})

This is the basic usage of the table sort. You can use this to display Queryset and also list of items.

.. note::
    The default text for the header when displaying data from a Queryset is the verbose_name of the field. For list of any other object you must set the header text using the column_names parameter.

Table CSS
*********

You can provide the css classes that the table should have as below.

.. code-block:: python

    from django.views.generic import ListView
    from django_table_sort.table import TableSort


    class ListViewExample(ListView):
        model = Person
        template_name: str = "base.html"
        ordering_key = "o"

        def get_ordering(self) -> tuple:
            return self.request.GET.getlist(self.ordering_key, None)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["table"] = TableSort(
                self.request,
                self.object_list,
                table_css_clases="table table-light table-striped table-sm",
                sort_key_name=self.ordering_key,
            )
            return context

Fields and exclude
******************

The default behavior is to show all fields of the model. If you want to show only certain field you can set this in the fields parameter as follows.

.. code-block:: python

    TableSort(request, object_list, fields=["name"])

This code will display only the field name in the table. You can also set which fields you don't want to display.

.. code-block:: python

    TableSort(request, object_list, exclude=["age"])

Any field you pass in the exclude parameter will not be display, and the others that aren't, will be.

.. warning::
    The current implementation looks first for the exclude field. So if you provide both fields and exclude, all the field no matter if is in the list of field you declared in the fields parameter **will not be displayed**.


Customizing fields headers
**************************

.. code-block:: python

    TableSort(request, object_list, fields=["age"], column_names={"age": "Age"})

You can set a custom header for any field. For this you can use the column_names parameter.

.. warning::
    If you set the fields and exclude parameter to None, and you provide the column_names
    parameter, all the fields that are given will be displayed.

Adding extra columns
********************

Sometimes you may want to add a custom column to the table column. You can do this using the added_columns parameter.

.. code-block:: python

    def sum(instance):
        return f"Sum {instance.age + 1}"


    TableSort(
        request,
        object_list,
        fields=["age"],
        column_names={"age": "Age"},
        added_columns=[(("added_column_1", "Sum"), sum)],
    )

The added_columns takes a list of tuples, following this pattern ((field_identifier, field_header), callable_function). The field_identifier is a str value to identify the field, the field_header to set the text of the header and the callable_function should be a function that takes one parameter and return a string value. The callable_function will be called for each row and the object that should be displayed is passed to as a parameter to the function.


List of items
*************

For list of items you need to set the column_names. All the field in the dictionary will be displayed.

.. code-block:: python

    TableSort(
        request,
        [person_1, person_2],
        fields=None,
        column_names={"age": "Age"},
    )

.. note::
    You can use the added_columns parameter to add other custom columns the same.

Primary key
***********

Sometimes you may want to show the primary key of your model, the default behavior is not to display the primary key of a Queryset since most of the time it is not useful to you this to the user.

.. code-block:: python

    TableSort(
        request,
        object_list,
        show_primary_key=True,
    )


Fields order
************

You can set the order to display the field in the table. For this you should use the field_order parameter.

.. code-block:: python

    TableSort(
        request,
        object_list,
        field_order=["age"],
    )

This will display the age as the first column in the table.

.. note::
    The field will be displayed following the order you give, but if you don't include a given field this
    will be displayed as the last. The field_order parameter works as a priority list.

To see the different options you can provide please see the section :ref:`table-sort-class`.
