from typing import Any

from datascribe_api.filter import Filter
from datascribe_api.models import (
    DataTableColumns,
    DataTableMetadata,
    DataTableRows,
    DataTableRowsCount,
    DataTables,
    MaterialByIdResults,
    MaterialSearchResults,
)

class DataScribeClient:
    def __init__(self, api_key: str | None = None, base: str = "https://datascribe.cloud/") -> None: ...
    def close(self) -> None: ...
    def search(self, endpoint: str, **kwargs: Any) -> Any: ...
    def get_data_tables(self) -> DataTables: ...
    def get_data_table(self, tableName: str, startingRow: int = 0, numRows: int = 100) -> DataTableRows: ...
    def get_data_tables_for_user(self) -> DataTables: ...
    def get_data_table_rows(
        self,
        tableName: str,
        columns: list[str],
        startingRow: int = 0,
        numRows: int = 100,
        filters: dict[str, Any] | Filter | list[Filter] | None = None,
    ) -> DataTableRows: ...
    def get_data_table_columns(self, tableName: str) -> DataTableColumns: ...
    def get_data_table_metadata(self, tableName: str) -> DataTableMetadata: ...
    def get_data_table_rows_count(
        self, tableName: str, filters: dict[str, Any] | Filter | list[Filter] | None = None
    ) -> DataTableRowsCount: ...
    def get_material_by_id(self, material_id: str, provider: list[str] | str) -> MaterialByIdResults: ...
    def search_materials(
        self,
        formula: str,
        elements: list[str] | str,
        exclude_elements: list[str] | str,
        spacegroup: str,
        props: list[str] | str,
        temperature: float,
        providers: list[str] | str,
        page: int = 1,
        size: int = 50,
    ) -> MaterialSearchResults: ...
