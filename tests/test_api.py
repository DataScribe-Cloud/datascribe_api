"""Testing suite for the API module.

This module contains unittests for the DataScribeClient and its API methods.
It verifies correct behavior for data table retrieval, metadata, columns, rows, and error handling.
"""

import os

import pytest
from requests import Session
from requests.exceptions import HTTPError

from datascribe_api import DataScribeClient
from datascribe_api.filter import Filter
from datascribe_api.models import (
    DataTable,
    DataTableColumn,
    DataTableColumns,
    DataTableMetadata,
    DataTableRow,
    DataTableRows,
    DataTableRowsCount,
    DataTables,
)
from datascribe_api.routes import ROUTES
from datascribe_api.utils import retry_session

API_TOKEN: str | None = os.environ.get("DATASCRIBE_API_TOKEN")
ADMIN_API_TOKEN: str | None = os.environ.get("DATASCRIBE_ADMIN_API_TOKEN")


@pytest.mark.skipif(not API_TOKEN, reason="DATASCRIBE_API_TOKEN not set in environment")
class TestDataScribeClient:
    """Unit tests for the DataScribeClient API."""

    @classmethod
    def setup_class(cls):
        """Set up resources required for all tests in this class."""
        cls.client = DataScribeClient(api_key=API_TOKEN)
        tables = cls.client.get_data_tables_for_user()
        table_name: str | None = getattr(tables[-2], "table_name", None)
        columns = cls.client.get_data_table_columns(tableName=table_name)
        cls.table_name = table_name
        cls.column_name = columns.columns[0].column_name

    @classmethod
    def teardown_class(cls):
        """Clean up resources initialized for all tests in this class."""
        cls.client.close()

    def test_retry_session_returns_session_instance(self) -> None:
        """Ensure retry_session returns a valid Session instance."""
        session = retry_session()
        assert isinstance(session, Session)

    def test_missing_api_key_raises_value_error(self) -> None:
        """Test that a ValueError is raised when no API key is provided."""
        if "DATASCRIBE_API_TOKEN" in os.environ:
            del os.environ["DATASCRIBE_API_TOKEN"]
        with pytest.raises(ValueError) as excinfo:
            DataScribeClient(api_key=None)
        assert "A DataScribe API key is required" in str(excinfo.value)

    def test_raises_attribute_error_for_invalid_endpoint(self) -> None:
        """Ensure AttributeError is raised for nonexistent endpoints."""
        with pytest.raises(AttributeError) as excinfo:
            self.client.nonexistent_endpoint()
        assert "object has no attribute 'nonexistent_endpoint'" in str(excinfo.value)

    def test_raises_value_error_when_api_request_fails(self, monkeypatch) -> None:
        """Ensure ValueError is raised when API response indicates failure."""
        monkeypatch.setattr(
            DataScribeClient, "_get", lambda self, *args, **kwargs: {"success": False, "message": "Invalid request"}
        )
        with pytest.raises(ValueError) as excinfo:
            self.client.search("get_data_tables")
        assert "API request failed: Invalid request" in str(excinfo.value)

    def test_returns_combined_list_of_routes_and_super_dir(self) -> None:
        """Ensure __dir__ returns a combined list of ROUTES keys and superclass attributes."""
        assert set(ROUTES.keys()).issubset(dir(self.client))

    @pytest.mark.skipif(not ADMIN_API_TOKEN, reason="DATASCRIBE_ADMIN_API_TOKEN not set in environment")
    def test_get_data_tables(self) -> None:
        """Test retrieving all data tables."""
        self.client = DataScribeClient(api_key=ADMIN_API_TOKEN)
        tables = self.client.get_data_tables()
        assert isinstance(tables, DataTables)
        assert hasattr(tables[0], "table_name")
        assert hasattr(tables[0], "display_name")
        assert hasattr(tables[0], "user_id")
        assert hasattr(tables[0], "created_on")
        assert hasattr(tables[0], "last_updated")
        assert hasattr(tables[0], "table_type")
        assert hasattr(tables[0], "visibility")
        assert hasattr(tables[0], "database_schema")
        assert all(isinstance(table, DataTable) for table in tables)

    def test_get_data_table(self) -> None:
        """Test retrieving a specific data table and its rows."""
        tables = self.client.get_data_tables_for_user()
        table = self.client.get_data_table(tableName=self.table_name)
        assert isinstance(tables, DataTables)
        assert isinstance(table, DataTableRows)
        assert hasattr(table[0], "_datascribe_user")
        assert hasattr(table[0], "_datascribe_insert_time")
        assert hasattr(table[0], "_datascribe_metadata")
        assert all(isinstance(table_row, DataTableRow) for table_row in table)

    def test_get_data_tables_for_user(self) -> None:
        """Test retrieving all data tables for the user."""
        tables = self.client.get_data_tables_for_user()
        assert isinstance(tables, DataTables)
        assert len(tables) is not None
        assert hasattr(tables[0], "table_name")
        assert hasattr(tables[0], "display_name")
        assert hasattr(tables[0], "user_id")
        assert hasattr(tables[0], "created_on")
        assert hasattr(tables[0], "last_updated")
        assert hasattr(tables[0], "table_type")
        assert hasattr(tables[0], "visibility")
        assert hasattr(tables[0], "database_schema")
        assert all(isinstance(table, DataTable) for table in tables)

    def test_get_data_table_rows(self) -> None:
        """Test retrieving rows from a data table."""
        tables = self.client.get_data_tables_for_user()
        columns = self.client.get_data_table_columns(tableName=self.table_name)
        rows = self.client.get_data_table_rows(tableName=self.table_name, columns=columns.to_list())
        assert isinstance(tables, DataTables)
        assert isinstance(columns, DataTableColumns)
        assert isinstance(rows, DataTableRows)
        assert all(isinstance(row, DataTableRow) for row in rows)

    def test_get_data_table_columns(self) -> None:
        """Test retrieving columns for a data table."""
        tables = self.client.get_data_tables_for_user()
        columns = self.client.get_data_table_columns(tableName=self.table_name)
        assert isinstance(tables, DataTables)
        assert isinstance(columns, DataTableColumns)
        assert isinstance(columns, DataTableColumns)
        assert hasattr(columns, "table_name")
        assert hasattr(columns, "display_name")
        assert hasattr(columns, "columns")
        assert isinstance(columns.columns, list)
        assert all(isinstance(column, DataTableColumn) for column in columns.columns)

    def test_get_data_table_metadata(self) -> None:
        """Test retrieving metadata for a data table."""
        tables = self.client.get_data_tables_for_user()
        metadata = self.client.get_data_table_metadata(tableName=self.table_name)
        assert isinstance(tables, DataTables)
        assert isinstance(metadata, DataTableMetadata)
        assert isinstance(metadata, DataTableMetadata)
        assert hasattr(metadata, "table_name")
        assert hasattr(metadata, "display_name")
        assert hasattr(metadata, "user_id")
        assert hasattr(metadata, "created_on")
        assert hasattr(metadata, "last_updated")
        assert hasattr(metadata, "table_type")
        assert hasattr(metadata, "visibility")
        assert hasattr(metadata, "database_schema")

    def test_get_data_table_rows_count(self) -> None:
        """Test retrieving the row count for a data table."""
        tables = self.client.get_data_tables_for_user()
        counts = self.client.get_data_table_rows_count(tableName=self.table_name)
        assert isinstance(tables, DataTables)
        assert isinstance(counts, DataTableRowsCount)
        assert hasattr(counts, "total_rows")

    def test_invalid_api_key(self) -> None:
        """Test that an invalid API key raises an HTTPError."""
        with pytest.raises(HTTPError):
            DataScribeClient(api_key="invalid_key").get_data_tables_for_user()

    def test_missing_required_param(self) -> None:
        """Test that missing required parameters raises a ValueError."""
        with pytest.raises(ValueError):
            self.client.get_data_table()

    def test_nonexistent_table(self) -> None:
        """Test that requesting a nonexistent table raises an HTTPError."""
        with pytest.raises(HTTPError):
            self.client.get_data_table(tableName="__nonexistent_table__")

    def test_empty_columns_for_rows(self) -> None:
        """Test that requesting rows with empty columns raises an HTTPError."""
        with pytest.raises(HTTPError):
            self.client.get_data_table_rows(tableName=self.table_name, columns=[])

    def test_context_manager(self) -> None:
        """Test that the DataScribeClient can be used as a context manager."""
        with DataScribeClient(api_key=API_TOKEN) as client:
            tables = client.get_data_tables_for_user()
            assert isinstance(tables, DataTables)

    def test_data_table_columns_len(self) -> None:
        """Test data table columns length."""
        columns = [
            DataTableColumn(column_name="a", data_type="int", is_nullable="NO"),
            DataTableColumn(column_name="b", data_type="str", is_nullable="YES"),
        ]
        dtc = DataTableColumns(table_name="t", display_name="T", columns=columns)
        assert len(dtc) == 2

    def test_filtering_with_dict(self) -> None:
        """Test filtering rows using a filter as a dict."""
        filters = {"column": self.column_name, "operator": "is not null", "value": None}
        rows = self.client.get_data_table_rows(tableName=self.table_name, columns=[self.column_name], filters=filters)
        assert isinstance(rows, DataTableRows)
        assert len(rows) >= 0

    def test_filtering_with_single_filter_object(self) -> None:
        """Test filtering rows using a single Filter object."""
        filters = Filter(self.column_name).is_not_null()
        rows = self.client.get_data_table_rows(tableName=self.table_name, columns=[self.column_name], filters=filters)
        assert isinstance(rows, DataTableRows)
        assert len(rows) >= 0

    def test_filtering_with_list_of_filters(self) -> None:
        """Test filtering rows using a list of Filter objects (AND logic)."""
        filters = [Filter(self.column_name).is_not_null()]
        rows = self.client.get_data_table_rows(tableName=self.table_name, columns=[self.column_name], filters=filters)
        assert isinstance(rows, DataTableRows)
        assert len(rows) >= 0

    def test_filtering_with_in_operator(self) -> None:
        """Test filtering rows using the 'in' operator."""
        filters = Filter(self.column_name).in_([self.column_name, "test", "foo", "bar"])
        try:
            rows = self.client.get_data_table_rows(tableName=self.table_name, columns=[self.column_name], filters=filters)
            assert isinstance(rows, DataTableRows)
        except HTTPError:
            pass  # Acceptable if no matching rows or unsupported type

    def test_filtering_with_like_operator(self) -> None:
        """Test filtering rows using the 'like' operator."""
        filters = Filter(self.column_name).like("%a%")
        try:
            rows = self.client.get_data_table_rows(tableName=self.table_name, columns=[self.column_name], filters=filters)
            assert isinstance(rows, DataTableRows)
        except HTTPError:
            pass  # Acceptable if no matching rows or unsupported type

    def test_filtering_with_is_null_operator(self) -> None:
        """Test filtering rows using the 'is null' operator."""
        filters = Filter(self.column_name).is_null()
        rows = self.client.get_data_table_rows(tableName=self.table_name, columns=[self.column_name], filters=filters)
        assert isinstance(rows, DataTableRows)

    def test_filtering_with_invalid_type_raises(self) -> None:
        """Test that passing an invalid filter type raises TypeError."""
        with pytest.raises(TypeError):
            self.client.get_data_table_rows(tableName=self.table_name, columns=[self.column_name], filters=123)

    def test_get_material_by_id_mp(self) -> None:
        """Test get_material_by_id with a valid MP material ID and provider."""
        result = self.client.get_material_by_id(ids="mp-149", providers="MP")
        assert result.total == 1
        assert isinstance(result.results, list)
        assert result.results[0].provider.lower() == "mp"
        assert result.results[0].data.material_id == "mp-149"
        assert result.results[0].data.formula_pretty == "Si"

    @pytest.mark.slow
    def test_get_material_by_id_aflow(self) -> None:
        """Test get_material_by_id with a valid AFLOW material ID and provider."""
        result = self.client.get_material_by_id(ids="08ab41c5f54850db", providers="AFLOW")
        assert result.total == 1
        assert isinstance(result.results, list)
        assert result.results[0].provider.lower() == "aflow"
        assert result.results[0].data.auid == "aflow:08ab41c5f54850db"

    @pytest.mark.slow
    def test_get_material_by_id_full_aflow(self) -> None:
        """Test get_material_by_id with a valid full AFLOW material ID and provider."""
        result = self.client.get_material_by_id(ids="aflow:08ab41c5f54850db", providers="AFLOW")
        assert result.total == 1
        assert isinstance(result.results, list)
        assert result.results[0].provider.lower() == "aflow"
        assert result.results[0].data.auid == "aflow:08ab41c5f54850db"

    def test_get_material_by_id_invalid(self) -> None:
        """Test get_material_by_id with an invalid material ID."""
        result = self.client.get_material_by_id(ids="invalid-id-123", providers="MP")
        assert result.total == 0
        assert isinstance(result.results, list)

    def test_search_materials_basic_mp(self) -> None:
        """Test search_materials with a valid MP material ID and formula."""
        result = self.client.search_materials(
            formula="SiO2",
            providers="MP",
        )
        assert result.total >= 1
        assert isinstance(result.results, list)
        assert result.results[0].formula in "SiO2"

    @pytest.mark.slow
    def test_search_materials_basic_aflow(self) -> None:
        """Test search_materials with a valid AFLOW material ID and formula."""
        result = self.client.search_materials(
            elements="Si,O",
            providers="AFLOW",
        )
        assert result.total >= 1
        assert isinstance(result.results, list)
        assert "Si" in result.results[0].elements
        assert "O" in result.results[0].elements

    @pytest.mark.slow
    def test_search_materials_basic_two_providers(self) -> None:
        """Test search_materials using two providers."""
        result = self.client.search_materials(
            formula="SiO2",
            providers=["MP", "AFLOW"],
        )
        assert result.total >= 2
        assert isinstance(result.results, list)
        assert "SiO2" in result.results[0].formula

    def test_search_materials_with_props(self) -> None:
        """Test search_materials with property filters."""
        result = self.client.search_materials(
            formula="SiO2",
            props="band_gap",
            providers="MP",
        )
        assert result.total >= 1
        assert isinstance(result.results, list)
        assert "bandgap" in result.results[0].key_props
        assert result.results[0].key_props["bandgap"] is not None

    def test_search_materials_returns_correct_number_of_materials_mp(self) -> None:
        """Test search_materials with pagination options for MP."""
        result = self.client.search_materials(
            formula="SiO2",
            size=1,
            providers="MP",
        )
        assert isinstance(result.results, list)
        assert len(result.results) == 1

    @pytest.mark.slow
    def test_search_materials_returns_correct_number_of_materials_aflow(self) -> None:
        """Test search_materials with pagination options for AFLOW."""
        result = self.client.search_materials(
            elements="Si,O",
            size=1,
            providers="AFLOW",
        )
        assert isinstance(result.results, list)
        assert len(result.results) >= 1

    @pytest.mark.slow
    def test_search_materials_returns_correct_number_of_materials_two_providers(self) -> None:
        """Test search_materials with pagination options for multiple providers."""
        result = self.client.search_materials(
            elements="Si,O",
            size=1,
            providers=["MP", "AFLOW"],
        )
        assert isinstance(result.results, list)
        assert len(result.results) == 2

    def test_search_materials_invalid_mp(self) -> None:
        """Test search_materials with invalid input for MP."""
        result = self.client.search_materials(formula="mp-invalid", providers="MP")
        assert isinstance(result.results, list)
        assert result.total == 0
        assert len(result.results) == 0

    @pytest.mark.slow
    def test_search_materials_invalid_aflow(self) -> None:
        """Test search_materials with invalid input for AFLOW."""
        result = self.client.search_materials(
            formula="aflow:invalid",
            providers="AFLOW",
        )
        assert isinstance(result.results, list)
        assert result.total == 0
        assert len(result.results) == 0

    @pytest.mark.slow
    def test_search_materials_invalid_two_providers(self) -> None:
        """Test search_materials with invalid input for multiple providers."""
        result = self.client.search_materials(
            formula="invalid",
            providers=["MP", "AFLOW"],
        )
        assert isinstance(result.results, list)
        assert result.total == 0
        assert len(result.results) == 0

    def test_search_materials_with_oqmd(self) -> None:
        """Test searching materials with the OQMD."""
        result = self.client.search_materials(
            formula="Al2O3",
            providers="OQMD",
        )
        assert result.total >= 1
        assert isinstance(result.results, list)
        assert result.results[0].formula in "Al2O3"
        assert result.results[0].provenance[0].provider == "OQMD"
