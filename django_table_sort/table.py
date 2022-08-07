from __future__ import annotations

from typing import Union

from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from django_table_sort.columns import TableColumn
from django_table_sort.columns import TableExtraColumn


class TableSort:
    """Class to generate the table with the sort."""

    def __init__(
        self,
        request: HttpRequest,
        object_list: QuerySet | list,
        column_names: None | dict[str, str] = None,
        sort_key_name: str = "o",
        column_css_clases: str = "text-center",
        table_css_clases: str = "table",
        table_id: str = None,
        **kwargs,
    ):
        self.request = request
        self.object_list = object_list
        self.sort_key_name = sort_key_name
        self.column_css_clases = column_css_clases
        self.table_css_clases = table_css_clases
        self.table_id = table_id
        self.kwargs = kwargs
        if column_names is None and isinstance(object_list, QuerySet):
            self.column_names = [
                TableColumn(field.name, field.verbose_name.title())
                for field in object_list.model._meta.fields
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
            url_start = self.request.GET.urlencode()
            sort_url = self.request.GET.urlencode()
            order_up = True
            first_sort = True
            if f"o=-{field_to_sort}" in sort_url:
                first_sort = False
                sort_url = sort_url.replace(
                    f"&o=-{field_to_sort}", f"&o={field_to_sort}"
                )
                sort_url = sort_url.replace(f"o=-{field_to_sort}", f"o={field_to_sort}")
                url_start = url_start.replace(f"&o=-{field_to_sort}", "")
                url_start = url_start.replace(f"o=-{field_to_sort}", "")
            elif f"o={field_to_sort}" in sort_url:
                order_up = False
                first_sort = False
                sort_url = sort_url.replace(
                    f"&o={field_to_sort}", f"&o=-{field_to_sort}"
                )
                sort_url = sort_url.replace(f"o={field_to_sort}", f"o=-{field_to_sort}")
                url_start = url_start.replace(f"&o={field_to_sort}", "")
                url_start = url_start.replace(f"o={field_to_sort}", "")
            else:
                sort_url = (
                    (sort_url + "&")
                    if len(sort_url) > 1 and not sort_url.endswith("&")
                    else sort_url
                )
                sort_url += f"o={field_to_sort}"
            url_start = url_start if not url_start.startswith("&") else url_start[1:]
            url_start = (
                url_start
                if not url_start.endswith("&")
                else url_start[: len(url_start) - 1]
            )
            headers_str += """
                <th class="column-sorted {classes}">
                    <div>
                        {column_name}
                        <div class="sort-options {show_sort}">
                            <a href="?{sort_url}" role="button" title="{ordering_text}"><i class="fa-solid fa-sort{sort_direction}"></i></a>
                        </div>
                        <div class="sort-options">
                            <a href="?{url_start}" class="{hide_cancel}" role="button" title="Remove sort"><i class="fa-solid fa-ban"></i></a>
                        </div>
                    </div>
                </th>""".format(  # noqa: F522
                url_start=url_start,
                sort_direction="" if first_sort else "-up" if not order_up else "-down",
                field_to_sort=field_to_sort,
                column_name=column_name,
                ordering_text=f"Sort by {column_name}" if first_sort else "Toggle sort",
                classes=self.column_css_clases,
                hide_cancel="hidden" if first_sort else "",
                show_sort="show" if not first_sort else "",
                sort_url=sort_url,
            )
        return headers_str
