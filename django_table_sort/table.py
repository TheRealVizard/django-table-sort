from __future__ import annotations

from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from django_table_sort.columns import TableColumn
from django_table_sort.columns import TableExtraColumn

ALL_FIELDS = ["__all__"]


class TableSort:
    """
    Class to generate the table with the sort.

    :param request: current ``HttpRequest`` to get the url lookups to create the links.
    :param object_list: ``QuerySet`` or ``list`` to fill the table.
    :param fields: ``list`` This field sets which fields should be displayed, the
        default value is ["__all__"] that will display all the fields in the model
        and the verbose_name of them as the header of the columns. You can use the
        column_names param to customize the headers.
    :param exclude: ``list`` Similar to the fields param, defines which fields
        should be excluded, all the field that aren't in the exclude list
        will be displayed.
    :param column_names: ``dict`` containing the pair
        {field_name: field_header}, this field has two uses, if you provide
        a ``list`` of X items this field will set which field
        will be displayed and the proper headers, if you provide
        a ``Queryset`` instead this field will define how the
        columns header will be displayed.
    :param sort_key_name: ``str`` for the key name that will be used to create
        the sort lookup in the urls.
    :param table_css_clases: class to be applied to the table.
    :param table_id: ``str`` for the id of the generated tabled.
    :param **kwargs: See below

    :Keyword Arguments:
        *show_primary_key* (``bool``) --
          Set if the primary key of the model should be displayed, default=``False``.
        *added_columns* (``list``) --
          Extra columns to show in the table, should be a ``list`` object
          having the pair ((field_identifier, field_header), callable_function).
          Note that field_identifier is to mark a difference to the models fields
          and callable_function needs to be a function that will receive an
          object and return an str to print in the table column.
    """

    def __init__(
        self,
        request: HttpRequest,
        object_list: QuerySet | list,
        fields: list = ALL_FIELDS,
        exclude: list = None,
        column_names: None | dict[str, str] = None,
        sort_key_name: str = "o",
        table_css_clases: str = "table",
        table_id: str = None,
        **kwargs,
    ):
        self.request = request
        self.object_list = object_list
        self.sort_key_name = sort_key_name
        self.table_css_clases = table_css_clases
        self.table_id = table_id
        self.kwargs = kwargs
        column_names = column_names or {}
        if exclude is not None and isinstance(object_list, QuerySet):
            fields = [
                field
                for field in object_list.model._meta.get_fields()
                if field.name not in exclude
            ]
            self.column_names = [
                TableColumn(
                    field.name, column_names.get(field.name, field.verbose_name.title())
                )
                for field in fields
                if not field.primary_key or kwargs.get("show_primary_key", False)
            ]
        elif fields is not None and isinstance(object_list, QuerySet):
            if fields == ALL_FIELDS:
                fields = object_list.model._meta.get_fields()
            else:
                fields = [
                    field
                    for field in object_list.model._meta.get_fields()
                    if field.name in fields
                ]
            self.column_names = [
                TableColumn(
                    field.name, column_names.get(field.name, field.verbose_name.title())
                )
                for field in fields
                if not field.primary_key or kwargs.get("show_primary_key", False)
            ]
        elif column_names is not None:
            self.column_names = [
                TableColumn(column_name, column_header)
                for column_name, column_header in column_names.items()
            ]
        else:
            self.column_names = []
        self.column_names += [
            TableExtraColumn(column_info[0], column_info[1], column_function)
            for column_info, column_function in self.kwargs.get("added_columns", [])
        ]

    def __str__(self):
        """Returns the table in HTML format."""
        return self.render()

    def render(self) -> str:
        """Generate the table with the sort."""

        return format_html(
            """
            <table{table_id}{table_clases}>
                <thead>
                    <tr>
                        {headers}
                    </tr>
                </thead>
                <tbody>
                    {body}
                </tbody>
            </table>
            """.format(
                body=self.get_table_body(),
                headers=self.get_table_headers(),
                table_clases=str(f' class="{self.table_css_clases}"')
                if self.table_css_clases is not None
                else "",
                table_id=f' id="{self.table_id}"' if self.table_id is not None else "",
            )
        )

    def get_table_body(self) -> str:
        """Generate the body of the table."""
        body_str: str = ""
        for obj in self.object_list:
            row_str: str = ""
            for column in self.column_names:
                if isinstance(column, TableColumn):
                    row_str += f"<td>{column.get_value(obj)}</td>"
                if isinstance(column, TableExtraColumn):
                    row_str += f"<td>{column.get_value(obj)}</td>"
            body_str += f"<tr>{row_str}</tr>"
        return body_str

    def get_table_headers(self) -> str:
        """Generate the column with the link to sort."""
        headers_str: str = ""
        for column in self.column_names:
            if isinstance(column, TableExtraColumn):
                headers_str += f"<th>{column.column_header}</th>"
                continue
            field_to_sort, column_name = column.column_field, column.column_header
            sort_url, remove_sort_url, first_sort, descending = self.get_sort_url(
                field_to_sort
            )
            headers_str += """
                <th class="column-sorted">
                    <div>
                        {column_name}
                        <div class="sort-options {show_sort}">
                            <a href="?{sort_url}" role="button" title="{ordering_text}">
                                <i class="fa-solid fa-sort{sort_direction}"></i>
                            </a>
                        </div>
                        <div class="sort-options">
                            <a href="?{remove_sort_url}"
                                class="{hide_cancel}"
                                role="button"
                                title="Remove sort">
                                    <i class="fa-solid fa-ban"></i>
                            </a>
                        </div>
                    </div>
                </th>""".format(  # noqa: F522
                remove_sort_url=remove_sort_url,
                sort_direction=""
                if first_sort
                else "-up"
                if not descending
                else "-down",
                field_to_sort=field_to_sort,
                column_name=column_name,
                ordering_text=f"Sort by {column_name}" if first_sort else "Toggle sort",
                hide_cancel="hidden" if first_sort else "",
                show_sort="show" if not first_sort else "",
                sort_url=sort_url,
            )
        return headers_str

    def contains_field(self, lookups, field):
        try:
            return lookups.index(field)
        except ValueError:
            return -1

    def get_sort_url(self, field):
        lookups = self.request.GET.copy()
        removed_lookup = self.request.GET.copy()

        first_sort = True
        descending = True

        if self.sort_key_name in lookups.keys():
            current_order = lookups.getlist(self.sort_key_name, [])
            removed_order = current_order.copy()
            position = self.contains_field(current_order, field)
            if position != -1:
                first_sort = False
                descending = False
                current_order[position] = f"-{field}"
                removed_order.remove(field)
            else:
                position = self.contains_field(current_order, f"-{field}")
                if position != -1:
                    first_sort = False
                    current_order[position] = field
                    removed_order.remove(f"-{field}")
                else:
                    current_order.append(field)
            lookups.setlist(self.sort_key_name, current_order)
            if len(removed_order) >= 1:
                removed_lookup.setlist(self.sort_key_name, removed_order)
            else:
                removed_lookup.pop(self.sort_key_name)
        else:
            lookups.setlist(self.sort_key_name, [field])

        return (
            lookups.urlencode(),
            removed_lookup.urlencode(),
            first_sort,
            descending,
        )
