"""Testing suite for the CLI module.

This module contains unittests for the datascribe_cli Typer CLI commands.
It verifies correct behavior for data table retrieval, metadata, columns, rows, and error handling.
"""

import json
import os
import re
import unittest

from typer.testing import CliRunner

from datascribe_cli.cli import app

API_TOKEN = os.environ.get("DATASCRIBE_API_TOKEN")
runner = CliRunner()


@unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
class TestDataScribeCLI(unittest.TestCase):
    """Unit tests for the datascribe_cli Typer CLI."""

    def setUp(self):
        """Set up a table_name for use in tests."""
        result = runner.invoke(app, ["data-tables-for-user", "--api-key", API_TOKEN, "--json"])
        self.assertEqual(result.exit_code, 0)
        json_objects = re.findall(r"\{.*?\}(?=\s*\{|\s*$)", result.output, flags=re.DOTALL)
        parsed_data = [json.loads(obj) for obj in json_objects]
        self.table_name = parsed_data[-1].get("table_name")  # FIXME
        self.assertIsNotNone(self.table_name)

    # def test_data_tables(self):
    #     """Test retrieving all data tables."""
    #     result = runner.invoke(app, ["data-tables", "--api-key", API_TOKEN])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertIn("table_name", result.output)

    def test_data_tables_for_user(self):
        """Test retrieving all data tables for the user."""
        result = runner.invoke(app, ["data-tables-for-user", "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("table_name", result.output)

    def test_data_table(self):
        """Test retrieving a specific data table."""
        result = runner.invoke(app, ["data-table", self.table_name, "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRows", result.output)
        self.assertIn("DataTableRow", result.output)
        self.assertIn("_datascribe_user", result.output)
        self.assertIn("_datascribe_insert_time", result.output)
        self.assertIn("_datascribe_metadata", result.output)

    def test_data_table_columns(self):
        """Test retrieving columns for a data table."""
        result = runner.invoke(app, ["data-table-columns", self.table_name, "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableColumns", result.output)
        self.assertIn("table_name", result.output)
        self.assertIn("display_name", result.output)
        self.assertIn("column_name", result.output)

    def test_data_table_metadata(self):
        """Test retrieving metadata for a data table."""
        result = runner.invoke(app, ["data-table-metadata", self.table_name, "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableMetadata", result.output)
        self.assertIn("table_name", result.output)
        self.assertIn("display_name", result.output)
        self.assertIn("user_id", result.output)
        self.assertIn("created_on", result.output)
        self.assertIn("last_updated", result.output)
        self.assertIn("table_type", result.output)
        self.assertIn("visibility", result.output)

    def test_data_table_rows_count(self):
        """Test retrieving the row count for a data table."""
        result = runner.invoke(app, ["data-table-rows-count", self.table_name, "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("DataTableRowsCount" in result.output)
        self.assertTrue("total_rows" in result.output)

    def test_data_table_rows(self):
        """Test retrieving rows from a data table."""
        result_cols = runner.invoke(app, ["data-table-columns", self.table_name, "--api-key", API_TOKEN, "--json"])
        self.assertEqual(result_cols.exit_code, 0)
        json_objects = re.findall(r"\{.*?\}(?=\s*\{|\s*$)", result_cols.output, flags=re.DOTALL)
        parsed_data = json.loads(json_objects[0])
        if not parsed_data:
            self.skipTest("No columns available to test data-table-rows.")
        column_names = [column.get("column_name") for column in parsed_data.get("columns")]
        if not column_names:
            self.skipTest("No columns found for table to test data-table-rows.")
        columns_arg = ",".join(column_names)
        result = runner.invoke(app, ["data-table-rows", self.table_name, columns_arg, "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRow", result.output)

    def test_invalid_api_key(self):
        """Test that an invalid API key returns an error."""
        result = runner.invoke(app, ["data-tables-for-user", "--api-key", "invalid_key"])
        self.assertIn("Error", result.output)
        self.assertIn("Unauthorized", result.output)
        self.assertIn("Invalid API key", result.output)

    def test_missing_required_param(self):
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing argument", result.output)

    def test_nonexistent_table(self):
        """Test that requesting a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table", "__nonexistent_table__", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)

    def test_empty_columns_for_rows(self):
        """Test that requesting rows with empty columns returns an error."""
        result = runner.invoke(app, ["data-table-rows", self.table_name, "", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("Missing required parameter", result.output)
        self.assertIn("columns", result.output)

    def test_help(self):
        """Test that the CLI help command works."""
        result = runner.invoke(app, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Datascribe CLI", result.output)


if __name__ == "__main__":
    unittest.main()
