from typing import Callable
from typing import Dict
from typing import Optional

from django.db.models import Model

EMPTY_COLUMN = "EMPTY-COLUMN"


class BaseColumn:
    def __init__(
        self,
        column_field: str,
        column_header: str,
        css_classes: Optional[Dict] = None,
    ) -> None:
        self.column_field = column_field
        self.column_header = column_header
        css_classes = css_classes or {}
        self.css_classes = css_classes.get(column_field, "")

    def get_value(self, instance: Model):
        """Return the column value for a given instance."""
        return getattr(instance, self.column_field)

    def classes(self) -> str:
        return self.css_classes


class TableColumn(BaseColumn):
    pass


class TableExtraColumn(BaseColumn):
    def __init__(
        self,
        column_field: str,
        column_header: str,
        function: Callable,
        css_classes: Optional[Dict] = None,
    ) -> None:
        super().__init__(column_field, column_header, css_classes)
        self.function = function

    def get_value(self, instance: Model):
        """Return the column value for a given instance."""
        return self.function(instance)


class EmptyColumn(BaseColumn):
    def get_value(self, instance: Model):
        return ""
