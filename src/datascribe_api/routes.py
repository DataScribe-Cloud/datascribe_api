"""Routes for the Datascribe API.

This module defines the API endpoints and their corresponding models for the Datascribe API.
"""

from datascribe_api.models import (
    DataTable,
    DataTableColumns,
    DataTableMetadata,
    DataTableRow,
    DataTableRowsCount,
)

ROUTES = {
    "get_data_tables": ("/data-tables", DataTable, []),
    "get_data_table": ("/data-table", DataTableRow, ["tableName"]),
    "get_data_tables_for_user": ("/data-tables-for-user", DataTable, []),
    "get_data_table_rows": ("/data-table-rows", DataTableRow, ["tableName", "columns"]),
    "get_data_table_columns": ("/data-table-columns", DataTableColumns, ["tableName"]),
    "get_data_table_metadata": ("/data-table-metadata", DataTableMetadata, ["tableName"]),
    "get_data_table_rows_count": ("/data-table-rows-count", DataTableRowsCount, ["tableName"]),
}
