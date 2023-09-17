===============
Getting Started
===============

The Test Models
***************

For example purposes, we'll use a simplified book app. Here are our models.

.. code-block:: python

    # app/models.py


    class Person(models.Model):
        name = models.CharField(max_length=100, verbose_name="First Name")
        age = models.IntegerField(verbose_name="Age in Years")

        def __str__(self):
            return self.name

Basic Usage
***********

.. code-block:: python

    from django.shortcuts import render
    from django_table_sort.table import TableSort
    from app.models import Person


    def view(request):
        table = TableSort(request, Person.objects.all())
        return render(request, "template.html", context={"table": table})

This is the basic usage of the table sort. You can use this to display a Queryset and also a list of items.

.. note::

    The default text for the header when displaying data from a Queryset is the verbose_name of the field. For a list of any other object, you must set the header text using the column_names parameter.

Table CSS
*********

You can provide the CSS classes that the table should have as shown below.

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
                table_css_classes="table table-light table-striped table-sm",
                sort_key_name=self.ordering_key,
            )
            return context

Fields and Exclusion
*******************

The default behavior is to show all fields of the model. If you want to show only certain fields, you can set this in the fields parameter as follows.

.. code-block:: python

    TableSort(request, object_list, fields=["name"])

This code will display only the field "name" in the table. You can also set which fields you don't want to display.

.. code-block:: python

    TableSort(request, object_list, exclude=["age"])

Any field you pass in the exclude parameter will not be displayed, and the others that aren't will be.

.. warning::

    The current implementation looks for the exclude field first. So if you provide both fields and exclude, all the fields, no matter if they are in the list of fields you declared in the fields parameter, **will not be displayed**.

Customizing Fields Headers
**************************

.. code-block:: python

    TableSort(request, object_list, fields=["age"], column_names={"age": "Age"})

You can set a custom header for any field. For this, you can use the column_names parameter.

.. warning::

    If you set the fields and exclude parameters to None and you provide the column_names parameter, all the fields that are given will be displayed.

Adding Extra Columns
********************

Sometimes you may want to add a custom column to the table. You can do this using the added_columns parameter.

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

The added_columns parameter takes a list of tuples following this pattern: ((field_identifier, field_header), callable_function). The field_identifier is a string value to identify the field, the field_header is used to set the text of the header, and the callable_function should be a function that takes one parameter and returns a string value. The callable_function will be called for each row, and the object that should be displayed is passed as a parameter to the function.

List of Items
*************

For a list of items, you need to set the column_names. All the fields in the dictionary will be displayed.

.. code-block:: python

    TableSort(
        request,
        [person_1, person_2],
        fields=None,
        column_names={"age": "Age"},
    )

.. note::

    You can use the added_columns parameter to add other custom columns in the same way.

Primary Key
***********

Sometimes you may want to show the primary key of your model. The default behavior is not to display the primary key of a Queryset since it is often not useful to show this to the user.

.. code-block:: python

    TableSort(
        request,
        object_list,
        show_primary_key=True,
    )

Fields Order
************

You can set the order to display the fields in the table. For this, you should usethe field_order parameter.

.. code-block:: python

    TableSort(
        request,
        object_list,
        field_order=["age"],
    )

This will display the "age" as the first column in the table.

.. note::

    The fields will be displayed following the order you give, but if you don't include a given field, it will be displayed as the last. The field_order parameter works as a priority list.


Customizing the Table Template
****************************

You can customize the template used for generating the table by providing a different `template_name` parameter in the TableSort constructor. By default, the template used is `'django_table_sort/table.html'`. Here's an example:

.. code-block:: python

    TableSort(
        request,
        object_list,
        template_name="custom_template.html",
    )

In the above example, the `'custom_template.html'` file will be used instead of the default template for generating the table.

To create your custom template, you can copy the contents of the default template `'django_table_sort/table.html'` and modify it according to your needs.

To see the different options you can provide, please see the section :ref:`table-sort-class`.
