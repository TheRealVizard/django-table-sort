from unittest import TestCase

from django.db import models
from django_table_sort.table import TableSort


class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    age = models.IntegerField(verbose_name="Age in years")


class Test(TestCase):
    def test_table_class(self):
        table = TableSort(
            request=None,
            object_list=[],
            table_css_clases="table table-striped",
        )
        self.assertIn('<table class="table table-striped"', str(table))

    def test_table_columns(self):
        table = TableSort(
            request=None,
            object_list=Person.objects.none(),
        )
        table_columns = [
            (column.column_field, column.column_header) for column in table.column_names
        ]
        self.assertEqual(len(table_columns),2)
        self.assertIn(("name", "Full Name"), table_columns)
        self.assertIn(("age", "Age In Years"), table_columns)
