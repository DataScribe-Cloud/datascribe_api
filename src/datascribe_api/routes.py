"""Routes for the Datascribe API.

This module defines the API endpoints and their corresponding models for the Datascribe API.
"""

from datascribe_api.models import (
    DataTable,
    DataTableColumns,
    DataTableMetadata,
    DataTableRow,
    DataTableRowsCount,
    UserDataTable,
)

ROUTES = {
    "get_data_tables": ("/data-tables", DataTable, []),  # DONE
    "get_data_table": ("/data-table", DataTable, ["tableName"]),  # FIXME
    "get_data_tables_for_user": ("/data-tables-for-user", UserDataTable, []),
    "get_data_table_rows": ("/data-table-rows", DataTableRow, ["tableName", "columns"]),
    "get_data_table_columns": ("/data-table-columns", DataTableColumns, ["tableName"]),
    "get_data_table_metadata": ("/data-table-metadata", DataTableMetadata, ["tableName"]),  # DONE
    "get_data_table_rows_count": ("/data-table-rows-count", DataTableRowsCount, ["tableName"]),  # DONE
}
