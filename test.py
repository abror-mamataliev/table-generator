from lib.table import Table


def main():
    table_1 = Table(
        name="\"E-auksion\" орқали деҳқон хўжалиги юритиш учун ер майдонлари ажратилиши тўғрисида",
        table_data="utils/table_data.json",
        table_resolver="utils/table_resolver.json",
    )
    # merged_cells = table_1.get_merged_cells()
    header_data = table_1.get_header_data()
    # row_ranges = table_1.get_row_ranges()
    # print(merged_cells)
    print(header_data)
    # print(row_ranges)
    # table_2 = Table(
    #     name="\"E-auksion\" орқали деҳқон хўжалиги юритиш учун ажратилган ер майдонларига қишлоқ хўжалиги экинлари экилиши (ПҚ-20 свод)",
    #     table_data="utils/table_data.json",
    #     table_resolver="utils/table_resolver.json",
    # )
    # merged_cells = table_2.get_merged_cells()
    # row_ranges = table_2.get_row_ranges()
    # print(merged_cells)
    # print(row_ranges)


if __name__ == "__main__":
    main()
