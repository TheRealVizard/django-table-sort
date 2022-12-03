from django_table_sort.columns import EMPTY_COLUMN, EmptyColumn


class EmptyColumnGenerator:
    empty_column = 0

    def get_next_empty_column_key(self):
        """Return the next empty column key."""
        empty_column += 1
        return f"{EMPTY_COLUMN}_{empty_column}"

    def get_next_empty_column(self, column_header: str):
        """Return the next empty column."""
        return EmptyColumn(self.get_next_empty_column_key(), column_header)
