from django_table_sort.columns import EMPTY_COLUMN
from django_table_sort.columns import EmptyColumn


class EmptyColumnGenerator:
    empty_column = 0

    def get_next_empty_column_key_no_add(self):
        """Return the next empty column key."""
        return f"{EMPTY_COLUMN}-{self.empty_column + 1}"

    def get_next_empty_column_key(self):
        """Return the next empty column key."""
        self.empty_column += 1
        return f"{EMPTY_COLUMN}-{self.empty_column}"

    def get_next_empty_column(self, column_header: str):
        """Return the next empty column."""
        return EmptyColumn(self.get_next_empty_column_key(), column_header)
