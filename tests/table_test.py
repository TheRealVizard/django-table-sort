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
            column_names={},
            table_css_clases="table table-striped",
        )
        self.assertIn("<table class=&quot;table table-striped&quot;", str(table))

    def test_table_columns(self):
        table = TableSort(
            request=None,
            object_list=Person.objects.none(),
        )
        self.assertDictEqual(
            {"name": "Full Name", "age": "Age In Years"}, table.column_names
        )
