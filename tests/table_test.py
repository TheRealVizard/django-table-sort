from django.test import TestCase
from django_table_sort.table import TableSort

from tests.models import Person
from django.test import RequestFactory

class Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.person = Person.objects.create(name="John Doe", age=23)
        cls.request_factory = RequestFactory()
        cls.request = cls.request_factory.get("")

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
        self.assertEqual(len(table_columns), 2)
        self.assertIn(("name", "Full Name"), table_columns)
        self.assertIn(("age", "Age In Years"), table_columns)

    def test_table_basic(self):
        table = TableSort(
            request=self.request,
            object_list=Person.objects.all(),
        )
        table_columns = [
            (column.column_field, column.column_header) for column in table.column_names
        ]
        self.assertEqual(len(table_columns), 2)
        self.assertIn(("name", "Full Name"), table_columns)
        self.assertIn(("age", "Age In Years"), table_columns)
        result = table.render()
        self.assertIn(self.person.name, result)
        self.assertIn(str(self.person.age), result)
