from django.test import RequestFactory
from django.test import TestCase

from django_table_sort.columns import EMPTY_COLUMN
from django_table_sort.table import TableSort
from tests.models import Person


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

    def test_table_fields(self):
        table = TableSort(
            request=self.request, object_list=Person.objects.all(), fields=["name"]
        )
        table_columns = [
            (column.column_field, column.column_header) for column in table.column_names
        ]
        self.assertEqual(len(table_columns), 1)
        self.assertIn(("name", "Full Name"), table_columns)
        self.assertNotIn(("age", "Age In Years"), table_columns)
        result = table.render()
        self.assertIn(self.person.name, result)
        self.assertNotIn(str(self.person.age), result)

    def test_table_show_primary_field(self):
        table = TableSort(
            request=self.request,
            object_list=Person.objects.all(),
            show_primary_key=True,
        )
        table_columns = [
            (column.column_field, column.column_header) for column in table.column_names
        ]
        self.assertEqual(len(table_columns), 3)
        self.assertIn(("id", "Id"), table_columns)
        self.assertIn(("name", "Full Name"), table_columns)
        self.assertIn(("age", "Age In Years"), table_columns)
        result = table.render()
        self.assertIn(str(self.person.id), result)
        self.assertIn(self.person.name, result)
        self.assertIn(str(self.person.age), result)

    def test_table_exclude(self):
        table = TableSort(
            request=self.request, object_list=Person.objects.all(), exclude=["name"]
        )
        table_columns = [
            (column.column_field, column.column_header) for column in table.column_names
        ]
        self.assertEqual(len(table_columns), 1)
        self.assertNotIn(("name", "Full Name"), table_columns)
        self.assertIn(("age", "Age In Years"), table_columns)
        result = table.render()
        self.assertNotIn(self.person.name, result)
        self.assertIn(str(self.person.age), result)

    def test_table_single_field_sort(self):
        table = TableSort(
            request=self.request,
            object_list=Person.objects.all(),
        )
        result = table.render()
        self.assertIn("?o=name", result)
        self.assertIn("?o=age", result)
        table = TableSort(
            request=self.request_factory.get("?o=name"),
            object_list=Person.objects.all(),
        )
        result = table.render()
        self.assertIn("?o=-name", result)
        self.assertIn("?o=name&o=age", result)

    def test_table_multiple_field_sort(self):
        table = TableSort(
            request=self.request_factory.get("?page=1"),
            object_list=Person.objects.all(),
        )
        result = table.render()
        self.assertIn("?page=1&o=name", result)
        self.assertIn("?page=1&o=age", result)
        table = TableSort(
            request=self.request_factory.get("?page=1&o=name"),
            object_list=Person.objects.all(),
        )
        result = table.render()
        self.assertIn("?page=1&o=-name", result)
        self.assertIn("?page=1&o=name&o=age", result)

    def test_table_column_order(self):
        table = TableSort(
            request=self.request,
            object_list=Person.objects.all(),
        )
        result = table.render()
        age_column_pos = result.find("Age In Years")
        name_column_pos = result.find("Full Name")
        self.assertGreater(age_column_pos, name_column_pos)
        table = TableSort(
            request=self.request, object_list=Person.objects.all(), field_order=["age"]
        )
        result = table.render()
        age_column_pos = result.find("Age in years")
        name_column_pos = result.find("Full Name")
        self.assertGreater(name_column_pos, age_column_pos)
        table = TableSort(
            request=self.request,
            object_list=Person.objects.all(),
            field_order=["age", "name"],
            show_primary_key=True,
        )
        result = table.render()
        age_column_pos = result.find("Age in years")
        name_column_pos = result.find("Full Name")
        id_column_pos = result.find("Id")
        self.assertGreater(name_column_pos, age_column_pos)
        self.assertGreater(id_column_pos, name_column_pos)

    def test_table_empty_column_creation(self):
        table = TableSort(
            request=self.request,
            object_list=[],
            column_names={
                "filed1": "Field1",
                "EMPTY-COLUMN-1": "An EMPTY COLUMN1",
                "EMPTY-COLUMN-2": "An EMPTY COLUMN2",
            },
        )
        result = table.render()
        table_columns = [
            (column.column_field, column.column_header) for column in table.column_names
        ]
        self.assertEqual(len(table_columns), 3)
        self.assertIn(("filed1", "Field1"), table_columns)
        self.assertIn(("EMPTY-COLUMN-1", "An EMPTY COLUMN1"), table_columns)
        self.assertIn(("EMPTY-COLUMN-2", "An EMPTY COLUMN2"), table_columns)
        self.assertIn("<th>An EMPTY COLUMN1</th>", result)
        self.assertIn("<th>An EMPTY COLUMN2</th>", result)

    def test_table_empty_column_sort(self):
        table = TableSort(
            request=self.request,
            object_list=[],
            column_names={
                "filed1": "Field1",
                "EMPTY-COLUMN-1": "An EMPTY COLUMN1",
                "EMPTY-COLUMN-2": "An EMPTY COLUMN2",
            },
            field_order=[EMPTY_COLUMN, "filed1", EMPTY_COLUMN],
        )
        result = table.render()
        field1_column_pos = result.find("Field1")
        empty_col_1_pos = result.find("An EMPTY COLUMN1")
        empty_col_2_pos = result.find("An EMPTY COLUMN2")
        self.assertGreater(empty_col_2_pos, empty_col_1_pos)
        self.assertGreater(field1_column_pos, empty_col_1_pos)
        self.assertGreater(empty_col_2_pos, field1_column_pos)

    def test_table_header_css_classes(self):
        table = TableSort(
            request=self.request,
            object_list=[],
            column_names={
                "filed1": "Field1",
                "EMPTY-COLUMN-1": "An EMPTY COLUMN1",
                "EMPTY-COLUMN-2": "An EMPTY COLUMN2",
            },
            column_headers_css_classes={"filed1": "filed1-header-class"},
        )
        result = table.render()
        self.assertIn("filed1-header-class", result)
