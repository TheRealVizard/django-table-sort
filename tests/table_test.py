from unittest import TestCase

from django_table_sort.table import TableSort


class Test(TestCase):
    def test_table_class(self):
        table = TableSort(
            request=None,
            object_list=[],
            column_names={},
            table_css_clases="table table-striped",
        )
        self.assertIn("<table class=&quot;table table-striped&quot;", str(table))
