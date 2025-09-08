"""Testing suite for the API module.

This module contains unittests for the DataScribeClient and its API methods.
It verifies correct behavior for data table retrieval, metadata, columns, rows, and error handling.
"""

import os
import unittest
import unittest.mock

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


class TestDataScribeClient(unittest.TestCase):
    """Unit tests for the DataScribeClient API."""

    def setUp(self) -> None:
        """Set up a DataScribeClient instance for each test."""
        self.client = DataScribeClient(api_key=API_TOKEN)

    def tearDown(self) -> None:
        """Clean up the DataScribeClient instance after each test."""
        self.client.close()

    def _get_valid_table_and_column(self) -> tuple[str, str]:
        """Helper to get a valid table name and a column name for filtering tests.

        Returns:
            tuple: (table_name, column_name)

        Raises:
            unittest.SkipTest: If no valid table/column is found.
        """
        tables = self.client.get_data_tables_for_user()
        for table in tables:
            table_name = getattr(table, "table_name", None)
            if not table_name:
                continue
            columns = self.client.get_data_table_columns(tableName=table_name)
            if columns.columns:
                return table_name, columns.columns[0].column_name
        raise unittest.SkipTest("No valid table/column found for filtering tests.")

    def test_retry_session_returns_session_instance(self) -> None:
        """Ensure retry_session returns a valid Session instance."""
        session = retry_session()
        self.assertIsInstance(session, Session)

    def test_missing_api_key_raises_value_error(self) -> None:
        """Test that a ValueError is raised when no API key is provided."""
        if "DATASCRIBE_API_TOKEN" in os.environ:
            del os.environ["DATASCRIBE_API_TOKEN"]
        with self.assertRaises(ValueError) as cm:
            DataScribeClient(api_key=None)
        self.assertIn("A DataScribe API key is required", str(cm.exception))

    def test_raises_attribute_error_for_invalid_endpoint(self) -> None:
        """Ensure AttributeError is raised for nonexistent endpoints."""
        with self.assertRaises(AttributeError) as cm:
            self.client.nonexistent_endpoint()
        self.assertIn("object has no attribute 'nonexistent_endpoint'", str(cm.exception))

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_raises_value_error_when_api_request_fails(self) -> None:
        """Ensure ValueError is raised when API response indicates failure."""
        with unittest.mock.patch(
            "datascribe_api.client.DataScribeClient._get", return_value={"success": False, "message": "Invalid request"}
        ):
            with self.assertRaises(ValueError) as cm:
                self.client.search("get_data_tables")
            self.assertIn("API request failed: Invalid request", str(cm.exception))

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_returns_combined_list_of_routes_and_super_dir(self) -> None:
        """Ensure __dir__ returns a combined list of ROUTES keys and superclass attributes."""
        self.assertTrue(set(ROUTES.keys()).issubset(dir(self.client)))

    # @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    # def test_get_data_tables(self) -> None:
    #     """Test retrieving all data tables."""
    #     tables = self.client.get_data_tables()
    # self.assertIsInstance(tables, DataTables)
    # self.assertTrue(hasattr(tables[0], "table_name"))
    # self.assertTrue(hasattr(tables[0], "display_name"))
    # self.assertTrue(hasattr(tables[0], "user_id"))
    # self.assertTrue(hasattr(tables[0], "created_on"))
    # self.assertTrue(hasattr(tables[0], "last_updated"))
    # self.assertTrue(hasattr(tables[0], "table_type"))
    # self.assertTrue(hasattr(tables[0], "visibility"))
    # self.assertTrue(hasattr(tables[0], "database_schema"))
    # self.assertTrue(all(isinstance(table, DataTable) for table in tables))

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_get_data_table(self) -> None:
        """Test retrieving a specific data table and its rows."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, DataTables)
        table_name = getattr(tables[-2], "table_name", None)  # FIXME
        table = self.client.get_data_table(tableName=table_name)
        self.assertIsInstance(table, DataTableRows)
        self.assertTrue(hasattr(table[0], "_datascribe_user"))
        self.assertTrue(hasattr(table[0], "_datascribe_insert_time"))
        self.assertTrue(hasattr(table[0], "_datascribe_metadata"))
        self.assertTrue(all(isinstance(table_row, DataTableRow) for table_row in table))

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_get_data_tables_for_user(self) -> None:
        """Test retrieving all data tables for the user."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, DataTables)
        self.assertTrue(hasattr(tables[0], "table_name"))
        self.assertTrue(hasattr(tables[0], "display_name"))
        self.assertTrue(hasattr(tables[0], "user_id"))
        self.assertTrue(hasattr(tables[0], "created_on"))
        self.assertTrue(hasattr(tables[0], "last_updated"))
        self.assertTrue(hasattr(tables[0], "table_type"))
        self.assertTrue(hasattr(tables[0], "visibility"))
        self.assertTrue(hasattr(tables[0], "database_schema"))
        self.assertTrue(all(isinstance(table, DataTable) for table in tables))

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_get_data_table_rows(self) -> None:
        """Test retrieving rows from a data table."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, DataTables)
        table_name = getattr(tables[-2], "table_name", None)  # FIXME
        columns = self.client.get_data_table_columns(tableName=table_name)
        self.assertIsInstance(columns, DataTableColumns)
        column_list = [column.column_name for column in columns.columns]
        rows = self.client.get_data_table_rows(tableName=table_name, columns=column_list)
        self.assertIsInstance(rows, DataTableRows)
        self.assertTrue(all(isinstance(row, DataTableRow) for row in rows))

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_get_data_table_columns(self) -> None:
        """Test retrieving columns for a data table."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, DataTables)
        table_name = getattr(tables[-2], "table_name", None)  # FIXME
        columns = self.client.get_data_table_columns(tableName=table_name)
        self.assertIsInstance(columns, DataTableColumns)
        self.assertIsInstance(columns, DataTableColumns)
        self.assertTrue(hasattr(columns, "table_name"))
        self.assertTrue(hasattr(columns, "display_name"))
        self.assertTrue(hasattr(columns, "columns"))
        self.assertIsInstance(columns.columns, list)
        self.assertTrue(all(isinstance(column, DataTableColumn) for column in columns.columns))

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_get_data_table_metadata(self) -> None:
        """Test retrieving metadata for a data table."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, DataTables)
        table_name = getattr(tables[-2], "table_name", None)  # FIXME
        metadata = self.client.get_data_table_metadata(tableName=table_name)
        self.assertIsInstance(metadata, DataTableMetadata)
        self.assertIsInstance(metadata, DataTableMetadata)
        self.assertTrue(hasattr(metadata, "table_name"))
        self.assertTrue(hasattr(metadata, "display_name"))
        self.assertTrue(hasattr(metadata, "user_id"))
        self.assertTrue(hasattr(metadata, "created_on"))
        self.assertTrue(hasattr(metadata, "last_updated"))
        self.assertTrue(hasattr(metadata, "table_type"))
        self.assertTrue(hasattr(metadata, "visibility"))
        self.assertTrue(hasattr(metadata, "database_schema"))

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_get_data_table_rows_count(self) -> None:
        """Test retrieving the row count for a data table."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, DataTables)
        table_name = getattr(tables[-2], "table_name", None)  # FIXME
        counts = self.client.get_data_table_rows_count(tableName=table_name)
        self.assertIsInstance(counts, DataTableRowsCount)
        self.assertTrue(hasattr(counts, "total_rows"))

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_invalid_api_key(self) -> None:
        """Test that an invalid API key raises an HTTPError."""
        with self.assertRaises(HTTPError):
            DataScribeClient(api_key="invalid_key").get_data_tables_for_user()

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_missing_required_param(self) -> None:
        """Test that missing required parameters raises a ValueError."""
        with self.assertRaises(ValueError):
            self.client.get_data_table()

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_nonexistent_table(self) -> None:
        """Test that requesting a nonexistent table raises an HTTPError."""
        with self.assertRaises(HTTPError):
            self.client.get_data_table(tableName="__nonexistent_table__")

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_empty_columns_for_rows(self) -> None:
        """Test that requesting rows with empty columns raises an HTTPError."""
        tables = self.client.get_data_tables_for_user()
        table_name = getattr(tables[0], "table_name", None)
        with self.assertRaises(HTTPError):
            self.client.get_data_table_rows(tableName=table_name, columns=[])

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_context_manager(self) -> None:
        """Test that the DataScribeClient can be used as a context manager."""
        with DataScribeClient(api_key=API_TOKEN) as client:
            tables = client.get_data_tables_for_user()
            self.assertIsInstance(tables, DataTables)

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_filtering_with_dict(self) -> None:
        """Test filtering rows using a filter as a dict."""
        table_name, column_name = self._get_valid_table_and_column()
        filters = {"column": column_name, "operator": "is not null", "value": None}
        rows = self.client.get_data_table_rows(tableName=table_name, columns=[column_name], filters=filters)
        self.assertIsInstance(rows, DataTableRows)
        self.assertGreaterEqual(len(rows), 0)

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_filtering_with_single_filter_object(self) -> None:
        """Test filtering rows using a single Filter object."""
        table_name, column_name = self._get_valid_table_and_column()
        filters = Filter(column_name).is_not_null()
        rows = self.client.get_data_table_rows(tableName=table_name, columns=[column_name], filters=filters)
        self.assertIsInstance(rows, DataTableRows)
        self.assertGreaterEqual(len(rows), 0)

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_filtering_with_list_of_filters(self) -> None:
        """Test filtering rows using a list of Filter objects (AND logic)."""
        table_name, column_name = self._get_valid_table_and_column()
        filters = [Filter(column_name).is_not_null()]
        rows = self.client.get_data_table_rows(tableName=table_name, columns=[column_name], filters=filters)
        self.assertIsInstance(rows, DataTableRows)
        self.assertGreaterEqual(len(rows), 0)

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_filtering_with_in_operator(self) -> None:
        """Test filtering rows using the 'in' operator."""
        table_name, column_name = self._get_valid_table_and_column()
        filters = Filter(column_name).in_(["test", "foo", "bar"])
        try:
            rows = self.client.get_data_table_rows(tableName=table_name, columns=[column_name], filters=filters)
            self.assertIsInstance(rows, DataTableRows)
        except HTTPError:
            pass  # Acceptable if no matching rows or unsupported type

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_filtering_with_like_operator(self) -> None:
        """Test filtering rows using the 'like' operator."""
        table_name, column_name = self._get_valid_table_and_column()
        filters = Filter(column_name).like("%a%")
        try:
            rows = self.client.get_data_table_rows(tableName=table_name, columns=[column_name], filters=filters)
            self.assertIsInstance(rows, DataTableRows)
        except HTTPError:
            pass

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_filtering_with_is_null_operator(self) -> None:
        """Test filtering rows using the 'is null' operator."""
        table_name, column_name = self._get_valid_table_and_column()
        filters = Filter(column_name).is_null()
        try:
            rows = self.client.get_data_table_rows(tableName=table_name, columns=[column_name], filters=filters)
            self.assertIsInstance(rows, DataTableRows)
        except HTTPError:
            pass

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_filtering_with_between_operator(self) -> None:
        """Test filtering rows using the 'between' operator."""
        table_name, column_name = self._get_valid_table_and_column()
        filters = Filter(column_name).between(0, 100)
        try:
            rows = self.client.get_data_table_rows(tableName=table_name, columns=[column_name], filters=filters)
            self.assertIsInstance(rows, DataTableRows)
        except HTTPError:
            pass

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_filtering_with_invalid_type_raises(self) -> None:
        """Test that passing an invalid filter type raises TypeError."""
        table_name, column_name = self._get_valid_table_and_column()
        with self.assertRaises(TypeError):
            self.client.get_data_table_rows(tableName=table_name, columns=[column_name], filters=123)
