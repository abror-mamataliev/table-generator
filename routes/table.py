from app.blueprint import table
from views import table as table_views


@table.route("/generate-table", methods=["GET"])
def generate_table():
    return table_views.generate_table()
