from flask import (
    jsonify,
    redirect,
    render_template,
    request,
    url_for
)
from typing import Union

from lib.table import Table


def generate_table():
    kwargs: dict = request.args
    table: Table = Table(
        table_data="utils/table_data.json",
        table_resolver="utils/table_resolver.json",
        **kwargs
    )
    generated: Union[dict, str] = table.generate()
    if kwargs.get('format') == "json":
        return jsonify(generated)
    elif kwargs.get('format') == "html":
        title: str = table.get_title()
        return render_template("table.html", table=generated, title=title)
    elif kwargs.get('format') == "excel":
        return redirect(url_for("uploads", filename=generated))
