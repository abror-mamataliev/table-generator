from datetime import date
from lib.table import Table


def main():
    table_2 = Table(
        type="2",
        table_data="utils/table_data.json"
    )
    table_3 = Table(
        type="3",
        table_data="utils/table_data.json"
    )
    table_4 = Table(
        type="4",
        table_data="utils/table_data.json"
    )
    # merged_cells = table_1.get_merged_cells()
    # header_data = table_1.get_header_data()
    # row_ranges = table_1.get_row_ranges()
    # print(merged_cells)
    # print(header_data)
    # print(row_ranges)
    # table_2 = Table(
    #     type="2",
    #     table_data="utils/table_data.json"
    # )
    table_2.insert_data("utils/excel/2.xlsx", date(2022, 9, 15))
    table_3.insert_data("utils/excel/3.xlsx", date(2022, 9, 15))
    table_4.insert_data("utils/excel/4.xlsx", date(2022, 9, 15))
    # merged_cells = table_2.get_merged_cells()
    # row_ranges = table_2.get_row_ranges()
    # print(merged_cells)
    # print(row_ranges)
    # table_2.insert_data("utils/excel/2.xlsx", date(2022, 9, 15))


if __name__ == "__main__":
    main()
