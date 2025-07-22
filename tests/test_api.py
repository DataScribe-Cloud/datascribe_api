"""Testing suite for the API module.

This module contains unittests for the DataScribeClient and its API methods.
It verifies correct behavior for data table retrieval, metadata, columns, rows, and error handling.
"""

import os
import unittest

from requests.exceptions import HTTPError

from datascribe_api import DataScribeClient
from datascribe_api.models import (
    DataTable,
    DataTableColumns,
    DataTableMetadata,
    DataTableRow,
    DataTableRowsCount,
)

API_TOKEN = os.environ.get("DATASCRIBE_API_TOKEN")


@unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
class TestDataScribeClient(unittest.TestCase):
    """Unit tests for the DataScribeClient API."""

    def setUp(self):
        """Set up a DataScribeClient instance for each test."""
        self.client = DataScribeClient(api_key=API_TOKEN)

    def tearDown(self):
        """Clean up the DataScribeClient instance after each test."""
        self.client.close()

    # def test_get_data_tables(self):
    #     """Test retrieving all data tables."""
    #     tables = self.client.get_data_tables()
    #     self.assertIsInstance(tables, list)
    #     if tables:
    #         self.assertIsInstance(tables[0], DataTable)

    def test_get_data_table(self):
        """Test retrieving a specific data table and its rows."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, list)
        if tables:
            table_name = getattr(tables[-2], "table_name", None)  # FIXME
            table = self.client.get_data_table(tableName=table_name)
            self.assertIsInstance(table[0], DataTableRow)
            self.assertTrue(all(isinstance(table_row, DataTableRow) for table_row in table))
        else:
            self.skipTest("No tables available to test get_data_table.")

    def test_get_data_tables_for_user(self):
        """Test retrieving all data tables for the user."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, list)
        if tables:
            self.assertIsInstance(tables[0], DataTable)
            self.assertTrue(hasattr(tables[0], "table_name"))
            self.assertTrue(hasattr(tables[0], "display_name"))
            self.assertTrue(hasattr(tables[0], "user_id"))
            self.assertTrue(hasattr(tables[0], "created_on"))
            self.assertTrue(hasattr(tables[0], "last_updated"))
            self.assertTrue(hasattr(tables[0], "table_type"))
            self.assertTrue(hasattr(tables[0], "visibility"))
            self.assertTrue(hasattr(tables[0], "database_schema"))
            self.assertTrue(all(isinstance(table, DataTable) for table in tables))
        else:
            self.skipTest("No tables available to test get_data_tables_for_user.")

    def test_get_data_table_rows(self):
        """Test retrieving rows from a data table."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, list)
        if tables:
            table_name = getattr(tables[-2], "table_name", None)  # FIXME
            columns_list = self.client.get_data_table_columns(tableName=table_name)
            columns = [col.column_name for col in getattr(columns_list[0], "columns", [])]
            self.assertIsInstance(columns, list)
            if columns:
                rows = self.client.get_data_table_rows(tableName=table_name, columns=columns)
                self.assertIsInstance(rows, list)
                if rows:
                    self.assertTrue(all(isinstance(row, DataTableRow) for row in rows))
            else:
                self.skipTest("No columns found for table to test get_data_table_rows.")
        else:
            self.skipTest("No tables available to test get_data_table_rows.")

    def test_get_data_table_columns(self):
        """Test retrieving columns for a data table."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, list)
        if tables:
            table_name = getattr(tables[-2], "table_name", None)  # FIXME
            columns = self.client.get_data_table_columns(tableName=table_name)
            self.assertIsInstance(columns, list)
            if columns:
                self.assertIsInstance(columns[0], DataTableColumns)
                self.assertTrue(all(isinstance(column, DataTableColumns) for column in columns))
                self.assertTrue(hasattr(columns[0], "table_name"))
                self.assertTrue(hasattr(columns[0], "display_name"))
                self.assertTrue(hasattr(columns[0], "columns"))
                self.assertIsInstance(columns[0].columns, list)
            else:
                self.skipTest("No columns found for table to test get_data_table_columns.")
        else:
            self.skipTest("No tables available to test get_data_table_columns.")

    def test_get_data_table_metadata(self):
        """Test retrieving metadata for a data table."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, list)
        if tables:
            table_name = getattr(tables[-2], "table_name", None)  # FIXME
            metadata = self.client.get_data_table_metadata(tableName=table_name)
            self.assertIsInstance(metadata, list)
            if metadata:
                self.assertIsInstance(metadata[0], DataTableMetadata)
                self.assertTrue(hasattr(metadata[0], "table_name"))
                self.assertTrue(hasattr(metadata[0], "display_name"))
                self.assertTrue(hasattr(metadata[0], "user_id"))
                self.assertTrue(hasattr(metadata[0], "created_on"))
                self.assertTrue(hasattr(metadata[0], "last_updated"))
                self.assertTrue(hasattr(metadata[0], "table_type"))
                self.assertTrue(hasattr(metadata[0], "visibility"))
                self.assertTrue(hasattr(metadata[0], "database_schema"))
                self.assertTrue(all(isinstance(data, DataTableMetadata) for data in metadata))
            else:
                self.skipTest("No metadata found for table to test get_data_table_metadata.")
        else:
            self.skipTest("No tables available to test get_data_table_metadata.")

    def test_get_data_table_rows_count(self):
        """Test retrieving the row count for a data table."""
        tables = self.client.get_data_tables_for_user()
        self.assertIsInstance(tables, list)
        if tables:
            table_name = getattr(tables[-2], "table_name", None)  # FIXME
            counts = self.client.get_data_table_rows_count(tableName=table_name)
            if counts:
                self.assertIsInstance(counts, list)
                self.assertIsInstance(counts[0], DataTableRowsCount)
                self.assertTrue(hasattr(counts[0], "total_rows"))
                self.assertTrue(all(isinstance(count, DataTableRowsCount) for count in counts))
            else:
                self.skipTest("No row counts found for table to test get_data_table_rows_count.")
        else:
            self.skipTest("No tables available to test get_data_table_rows_count.")

    def test_invalid_api_key(self):
        """Test that an invalid API key raises an HTTPError."""
        with self.assertRaises(HTTPError):  # FIXME
            DataScribeClient(api_key="invalid_key").get_data_tables_for_user()

    def test_missing_required_param(self):
        """Test that missing required parameters raises a ValueError."""
        with self.assertRaises(ValueError):
            self.client.get_data_table()

    def test_nonexistent_table(self):
        """Test that requesting a nonexistent table raises an HTTPError."""
        with self.assertRaises(HTTPError):  # FIXME
            self.client.get_data_table(tableName="__nonexistent_table__")

    def test_empty_columns_for_rows(self):
        """Test that requesting rows with empty columns raises an HTTPError."""
        tables = self.client.get_data_tables_for_user()
        if tables:
            table_name = getattr(tables[0], "table_name", None)  # FIXME
            with self.assertRaises(HTTPError):  # FIXME
                self.client.get_data_table_rows(tableName=table_name, columns=[])
        else:
            self.skipTest("No tables available to test empty columns for rows.")

    def test_context_manager(self):
        """Test that the DataScribeClient can be used as a context manager."""
        with DataScribeClient(api_key=API_TOKEN) as client:
            tables = client.get_data_tables_for_user()
            self.assertIsInstance(tables, list)  # FIXME


if __name__ == "__main__":
    unittest.main()
