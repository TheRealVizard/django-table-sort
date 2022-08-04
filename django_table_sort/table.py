from typing import Union

from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html


class TableSort:
    """Class to generate the table with the sort."""

    def __init__(
        self,
        request: HttpRequest,
        object_list: Union[QuerySet, list],
        sort_key_name: str = "o",
        clases: str = "text-center",
        column_names: Union[None, dict[str, str]] = None,
    ):
        self.request = request
        self.object_list = object_list
        self.sort_key_name = sort_key_name
        self.clases = clases
        self.column_names = column_names

    def __str__(self):
        """Returns the table in HTML format."""
        return self.render()

    def render(self) -> str:
        """Generate the table with the sort."""

        return format_html(
            """
            <table>
                <thead>
                    <tr>
                        {headers}
                    </tr>
                </thead>
                <tbody>
                    {body}
                </tbody>
            </table>
            """,
            body=self.get_table_body(),
            headers=self.get_table_headers(),
        )

    def get_table_body(self) -> str:
        """Generate the body of the table."""
        body_str: str = ""
        for obj in self.object_list:
            row_str: str = ""
            for column_name in self.column_names.keys():
                row_str += f"<td>{getattr(obj,column_name)}</td>"
            body_str += f"<tr>{row_str}</tr>"
        return format_html(body_str)

    def get_table_headers(self) -> str:
        """Generate the column with the link to sort."""
        headers_str: str = ""
        for field_to_sort, column_name in self.column_names.items():
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
                classes=self.clases,
                hide_cancel="hidden" if first_sort else "",
                show_sort="show" if not first_sort else "",
                sort_url=sort_url,
            )
        return format_html(headers_str)
