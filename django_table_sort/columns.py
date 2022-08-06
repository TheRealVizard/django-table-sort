from typing import Callable

from django.db.models import Model


class BaseColumn:
    def __init__(self, column_field: str, column_header: str) -> None:
        self.column_field = column_field
        self.column_header = column_header

    def get_value(self, instance: Model):
        """Return the column value for a given instance."""
        return getattr(instance, self.column_field)


class TableColumn(BaseColumn):
    pass


class TableExtraColumn(BaseColumn):
    def __init__(
        self, column_field: str, column_header: str, function: Callable
    ) -> None:
        super().__init__(column_field, column_header)
        self.function = function

    def get_value(self, instance: Model):
        """Return the column value for a given instance."""
        return self.function(instance)
