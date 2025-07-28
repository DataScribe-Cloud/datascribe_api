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

API_TOKEN = os.environ.get("DATASCRIBE_API_TOKEN")


class TestDataScribeClient(unittest.TestCase):
    """Unit tests for the DataScribeClient API."""

    def setUp(self):
        """Set up a DataScribeClient instance for each test."""
        self.client = DataScribeClient(api_key=API_TOKEN)

    def tearDown(self):
        """Clean up the DataScribeClient instance after each test."""
        self.client.close()

    def test_retry_session_returns_session_instance(self):
        """Ensure retry_session returns a valid Session instance."""
        session = retry_session()
        self.assertIsInstance(session, Session)

    def test_missing_api_key_raises_value_error(self):
        """Test that a ValueError is raised when no API key is provided."""
        if "DATASCRIBE_API_TOKEN" in os.environ:
            del os.environ["DATASCRIBE_API_TOKEN"]
        with self.assertRaises(ValueError) as cm:
            DataScribeClient(api_key=None)
        self.assertIn("A DataScribe API key is required", str(cm.exception))

    def test_raises_attribute_error_for_invalid_endpoint(self):
        """Ensure AttributeError is raised for nonexistent endpoints."""
        with self.assertRaises(AttributeError) as cm:
            self.client.nonexistent_endpoint()
        self.assertIn("object has no attribute 'nonexistent_endpoint'", str(cm.exception))

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_raises_value_error_when_api_request_fails(self):
        """Ensure ValueError is raised when API response indicates failure."""
        with unittest.mock.patch(
            "datascribe_api.client.DataScribeClient._get", return_value={"success": False, "message": "Invalid request"}
        ):
            with self.assertRaises(ValueError) as cm:
                self.client.search("get_data_tables")
            self.assertIn("API request failed: Invalid request", str(cm.exception))

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_returns_combined_list_of_routes_and_super_dir(self):
        """Ensure __dir__ returns a combined list of ROUTES keys and superclass attributes."""
        self.assertTrue(set(ROUTES.keys()).issubset(dir(self.client)))

    # @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    # def test_get_data_tables(self):
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
    def test_get_data_table(self):
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
    def test_get_data_tables_for_user(self):
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
    def test_get_data_table_rows(self):
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
    def test_get_data_table_columns(self):
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
    def test_get_data_table_metadata(self):
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
    def test_get_data_table_rows_count(self):
        """Test retrieving the row count for a data table."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, DataTables)
        table_name = getattr(tables[-2], "table_name", None)  # FIXME
        counts = self.client.get_data_table_rows_count(tableName=table_name)
        self.assertIsInstance(counts, DataTableRowsCount)
        self.assertTrue(hasattr(counts, "total_rows"))

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_invalid_api_key(self):
        """Test that an invalid API key raises an HTTPError."""
        with self.assertRaises(HTTPError):
            DataScribeClient(api_key="invalid_key").get_data_tables_for_user()

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_missing_required_param(self):
        """Test that missing required parameters raises a ValueError."""
        with self.assertRaises(ValueError):
            self.client.get_data_table()

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_nonexistent_table(self):
        """Test that requesting a nonexistent table raises an HTTPError."""
        with self.assertRaises(HTTPError):
            self.client.get_data_table(tableName="__nonexistent_table__")

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_empty_columns_for_rows(self):
        """Test that requesting rows with empty columns raises an HTTPError."""
        tables = self.client.get_data_tables_for_user()
        table_name = getattr(tables[0], "table_name", None)
        with self.assertRaises(HTTPError):
            self.client.get_data_table_rows(tableName=table_name, columns=[])

    @unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
    def test_context_manager(self):
        """Test that the DataScribeClient can be used as a context manager."""
        with DataScribeClient(api_key=API_TOKEN) as client:
            tables = client.get_data_tables_for_user()
            self.assertIsInstance(tables, DataTables)


if __name__ == "__main__":
    unittest.main()
