from json import load
from openpyxl import (load_workbook)
from openpyxl.descriptors import Sequence
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.cell_range import MultiCellRange
from openpyxl.worksheet.worksheet import Worksheet
from typing import Union

from lib.sqlite import SQLite
from .exceptions import (
    TableAttributeError,
    TableValueError
)


class Table:

    def __init__(
        self,
        name: str = None,
        table_data: str = None,
        table_resolver: str = None,
        **kwargs
    ) -> None:
        if name is None:
            raise TableAttributeError("Table name is required.")
        if table_data is None:
            raise TableAttributeError("Table data is required.")
        if table_resolver is None:
            raise TableAttributeError("Table resolver is required.")
        self.name: str = name
        self._table_data: str = table_data
        self._table_resolver: str = table_resolver
        for key, value in kwargs.items():
            self.__dict__[f'_{key}'] = value
        self._type: str = self._get_type()
        self._table_data: dict = self._get_table_data()
    
    def _generate_excel(self, headers: list, data: list) -> str:
        pass

    def _generate_html(self, headers: list, data: list) -> str:
        table = "<table class='table table-bordered text-center'>"
        table += "<thead>"
        for row in headers:
            table += "<tr>"
            for header in row:
                table += f"<th colspan='{header['colspan']}' rowspan='{header['rowspan']}'>{header['name']}</th>"
            table += "</tr>"
        table += "</thead>"
        table += "<tbody>"
        # for key in data:
        #     table += "<tr>"
        #     for i in range(len(data[key])):
        #         value = data[key][i]
        #         if i == 0 and key == 'total':
        #             table += f"<td colspan='2'>{value}</td>"
        #         else:
        #             table += f"<td>{round(value) if isinstance(value, float) else value if value is not None else ''}</td>"
        #     table += "</tr>"
        table += "</tbody>"
        table += "</table>"
        return table

    def _generate_json(self, headers: list, data: list) -> dict:
        new_data: dict = {}
        index: int = 1
        for key in data:
            new_data[str(index)] = data[key]
            index += 1
        del index
        new_data['total'] = data['total']
        return {
            'headers': headers,
            'data': new_data
        }

    def _get_columns(self) -> list:
        return self._table_data['columns']

    def _get_column_keys(self) -> list:
        return self._table_data['column_keys']

    def _get_column_ranges(self) -> dict:
        merged_cells: list = self._get_merged_cells()
        column_ranges: dict = {
            'min': None,
            'max': None
        }
        workbook: Workbook = load_workbook(f"utils/excel/{self._type}.xlsx")
        worksheet: Worksheet = workbook["Жами"]
        columns = worksheet.columns
        for cell in merged_cells:
            if str(cell).startswith("A1:"):
                column_ranges['min'], column_ranges['max'] = [item[0] for item in cell.split(":")]
        # print(self._table_data['column_ranges'])
        workbook.close()
        return column_ranges

    def _get_data(self) -> dict:
        columns: list = self._get_columns()
        column_keys: list = self._get_column_keys()
        data: list = {}
        sql: SQLite = SQLite(f"database/excel/{self._type}.db")
        if '_region' in self.__dict__:
            region: str = sql.select(
                table="region",
                fields=["name"],
                where=f"id = {self._region}",
                first=True
            )[0]
            districts: list = sql.select(
                table="data",
                fields=["name", "district", "id"],
                where=f"region = '{region}'",
                group_by="district",
                order_by="id",
                first=False
            )
            for i in range(len(districts)):
                district = districts[i]
                row = []
                for column in columns:
                    type = column['type']
                    if type == "index":
                        row.append(i + 1)
                    elif type == "name":
                        row.append(district[0])
                    else:
                        row.append(None)
                data[district[1]] = row
            data['total'] = []
            for column in columns:
                type = column['type']
                if type == "index":
                    continue
                elif type == "name":
                    data['total'].append("Жами")
                else:
                    data['total'].append(None)
            for i in range(len(districts)):
                district = districts[i]
                result: list = sql.select(
                    table="data",
                    fields=["key", "value"],
                    where=f"region = '{region}' AND district = '{district[1]}' AND name = '{district[0]}'",
                    first=False
                )
                for item in result:
                    data[district[1]][column_keys[item[0]]] = item[1]
                    if data['total'][column_keys[item[0]] - 1] is None:
                        data['total'][column_keys[item[0]] - 1] = item[1]
                    else:
                        data['total'][column_keys[item[0]] - 1] += item[1]
        else:
            pass
        sql.close()
        for key in data:
            for i in range(len(data[key]) - 1, -1, -1):
                if key != 'total':
                    if columns[i]['type'] == "sum":
                        data[key][i] = sum(data[key][j] for j in columns[i]['indexes'])
                        if data['total'][i - 1] is None:
                            data['total'][i - 1] = data[key][i]
                        else:
                            data['total'][i - 1] += data[key][i]
        return data

    def _get_headers(self) -> list:
        return self._table_data['headers']

    def _get_header_data(self) -> list:
        workbook: Workbook = load_workbook(f"utils/excel/{self._type}.xlsx")
        worksheet: Worksheet = workbook["Жами"]
        merged_cells = self._get_merged_cells()
        column_ranges = self._get_column_ranges()
        row_ranges = self._get_row_ranges()
        header_data: list = []
        row = row_ranges['min']
        while row <= row_ranges['max']:
            header_row: list = []
            column = column_ranges['min']
            while column <= column_ranges['max']:
                merged_cell = None
                for cell in merged_cells:
                    cell_begin, cell_end = cell.split(":")
                    if str(cell).startswith(f"{column}{row}:") or cell_begin[0] <= column <= cell_end and int(cell_begin[1]) <= row <= int(cell_end[1]):
                        merged_cell = cell
                        break
                if merged_cell is not None:
                    merged_cell = [item for item in merged_cell.split(":")]
                    header_row.append({
                        'name': worksheet[f"{column}{row}"].value,
                        'colspan': ord(merged_cell[1][0]) - ord(merged_cell[0][0]) + 1,
                        'rowspan': int(merged_cell[1][1:]) - int(merged_cell[0][1:]) + 1
                    })
                else:
                    header_row.append({
                        'name': worksheet[f"{column}{row}"].value,
                        'colspan': 1,
                        'rowspan': 1
                    })
                column = chr(ord(column) + 1)
            print(header_row)
            header_data.append(header_row)
            row += 1
        workbook.close()

    def _get_merged_cells(self) -> list:
        workbook: Workbook = load_workbook(f"utils/excel/{self._type}.xlsx")
        worksheet: Worksheet = workbook["Жами"]
        merged_cells: MultiCellRange = worksheet.merged_cells
        merged_cells: Sequence = merged_cells.ranges
        merged_cells: list = [str(item) for item in merged_cells]
        merged_cells.sort()
        workbook.close()
        return merged_cells

    def _get_row_ranges(self) -> dict:
        merged_cells: list = self._get_merged_cells()
        row_ranges: dict = {
            'min': None,
            'max': None
        }
        workbook: Workbook = load_workbook(f"utils/excel/{self._type}.xlsx")
        worksheet: Worksheet = workbook["Жами"]
        for cell in merged_cells:
            cell_min, cell_max = (item for item in cell.split(":"))
            if int(cell_min[1:]) > 3 and worksheet[cell_min].value != "Жами":
                if row_ranges['min'] is None:
                    row_ranges['min'] = int(cell_min[1:])
                else:
                    row_ranges['min'] = min(row_ranges['min'], int(cell_min[1:]))
                if row_ranges['max'] is None:
                    row_ranges['max'] = int(cell_max[1:])
                else:
                    row_ranges['max'] = max(row_ranges['max'], int(cell_max[1:]))
        workbook.close()
        return row_ranges

    def _get_table_data(self) -> dict:
        with open(self._table_data, "r", encoding="utf-8") as file:
            return load(file)[self._type]

    def _get_type(self) -> str:
        with open(self._table_resolver, "r", encoding="utf-8") as file:
            return load(file)[self.name]

    def generate(self) -> Union[str, dict]:
        if '_format' not in self.__dict__:
            raise TableAttributeError("Table format is required.")
        try:
            generate_method = getattr(self, f"_generate_{self._format}")
            headers: list = self._get_headers()
            data: list = {}
            # data: list = self._get_data()
            return generate_method(headers, data)
        except:
            raise TableValueError(f"\"{self._format}\" format is not supported.")

    def get_column_ranges(self) -> dict:
        return self._get_column_ranges()

    def get_header_data(self) -> list:
        return self._get_header_data()

    def get_merged_cells(self) -> list:
        return self._get_merged_cells()
    
    def get_row_ranges(self) -> dict:
        return self._get_row_ranges()
