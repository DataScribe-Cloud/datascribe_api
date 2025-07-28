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
        result_table = runner.invoke(app, ["data-tables-for-user", "--api-key", API_TOKEN, "--json"])
        self.assertEqual(result_table.exit_code, 0)
        json_objects = re.findall(r"\{.*?\}(?=\s*\{|\s*$)", result_table.output, flags=re.DOTALL)
        parsed_data = [json.loads(obj) for obj in json_objects]
        self.table_name = parsed_data[-1].get("table_name")  # FIXME
        self.assertIsNotNone(self.table_name)

        result_cols = runner.invoke(app, ["data-table-columns", self.table_name, "--api-key", API_TOKEN, "--json"])
        self.assertEqual(result_cols.exit_code, 0)
        json_objects_cols = re.findall(r"\{.*?\}(?=\s*\{|\s*$)", result_cols.output, flags=re.DOTALL)
        parsed_data_cols = json.loads(json_objects_cols[0])
        column_names = [column.get("column_name") for column in parsed_data_cols.get("columns")]
        self.columns_arg = ",".join(column_names[:3])
        self.assertIsNotNone(self.columns_arg)

    # def test_data_tables(self):
    #     """Test retrieving all data tables."""
    #     result = runner.invoke(app, ["data-tables", "--api-key", API_TOKEN])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertIn("table_name", result.output)
    #
    # def test_data_tables_json(self):
    #     """Test retrieving all data tables with JSON output."""
    #     result = runner.invoke(app, ["data-tables", "--api-key", API_TOKEN, "--json"])
    #     self.assertEqual(result.exit_code, 0)
    #     self.assertNotIn("table_name", result.output)

    def test_data_tables_insufficient_permissions(self):
        """Test that insufficient permissions returns an error."""
        # This test assumes that the API token used does not have permission to access data tables.
        result = runner.invoke(app, ["data-tables", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("Forbidden", result.output)
        self.assertIn("User is not a datascribe manager", result.output)

    def test_data_tables_for_user(self):
        """Test retrieving all data tables for the user."""
        result = runner.invoke(app, ["data-tables-for-user", "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("table_name", result.output)

    def test_data_tables_for_user_invalid_api_key(self):
        """Test that an invalid API key returns an error."""
        result = runner.invoke(app, ["data-tables-for-user", "--api-key", "invalid_key"])
        self.assertIn("Error", result.output)
        self.assertIn("Unauthorized", result.output)
        self.assertIn("Invalid API key", result.output)

    def test_data_table(self):
        """Test retrieving a specific data table."""
        result = runner.invoke(app, ["data-table", self.table_name, "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRows", result.output)
        self.assertIn("DataTableRow", result.output)
        self.assertIn("_datascribe_user", result.output)
        self.assertIn("_datascribe_insert_time", result.output)
        self.assertIn("_datascribe_metadata", result.output)

    def test_data_table_missing_required_param(self):
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing argument", result.output)

    def test_data_table_nonexistent_table(self):
        """Test that requesting a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table", "__nonexistent_table__", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 500", result.output)

    def test_data_table_outputs_json_representation_when_json_flag_is_true(self):
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(app, ["data-table", self.table_name, "--api-key", API_TOKEN, "--json"])
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn("DataTableRows", result.output)
        self.assertNotIn("DataTableRow", result.output)

    def test_data_table_columns(self):
        """Test retrieving columns for a data table."""
        result = runner.invoke(app, ["data-table-columns", self.table_name, "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableColumns", result.output)
        self.assertIn("table_name", result.output)
        self.assertIn("display_name", result.output)
        self.assertIn("column_name", result.output)

    def test_data_table_columns_missing_required_param(self):
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table-columns"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing argument", result.output)

    def test_data_table_columns_nonexistent_table(self):
        """Test that requesting columns for a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table-columns", "__nonexistent_table__", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 500", result.output)

    def test_data_table_columns_outputs_json_representation_when_json_flag_is_true(self):
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(app, ["data-table-columns", self.table_name, "--api-key", API_TOKEN, "--json"])
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn("DataTableColumns", result.output)
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

    def test_data_table_metadata_missing_required_param(self):
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table-metadata"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing argument", result.output)

    def test_data_table_metadata_nonexistent_table(self):
        """Test that requesting metadata for a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table-metadata", "__nonexistent_table__", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 500", result.output)

    def test_data_table_metadata_outputs_json_representation_when_json_flag_is_true(self):
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(app, ["data-table-metadata", self.table_name, "--api-key", API_TOKEN, "--json"])
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn("DataTableMetadata", result.output)
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
        self.assertIn("DataTableRowsCount", result.output)
        self.assertIn("total_rows", result.output)

    def test_data_table_rows_count_nonexistent_table(self):
        """Test that requesting row count for a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table-rows-count", "__nonexistent_table__", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 500", result.output)

    def test_data_table_rows_count_outputs_json_representation_when_json_flag_is_true(self):
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(app, ["data-table-rows-count", self.table_name, "--api-key", API_TOKEN, "--json"])
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn("DataTableRowsCount", result.output)
        self.assertIn("total_rows", result.output)

    def test_data_table_rows_count_missing_required_param(self):
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table-rows-count"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing argument", result.output)

    def test_data_table_rows(self):
        """Test retrieving rows from a data table."""
        result = runner.invoke(
            app,
            ["data-table-rows", "nimplex_composition_space", "Node_ID,NodeCoord_0,NodeCoord_1", "--api-key", API_TOKEN],
        )  # FIXME
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRow", result.stdout)

    def test_data_table_rows_missing_required_param(self):
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table-rows"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing argument", result.output)

    def test_data_table_rows_nonexistent_table(self):
        """Test that requesting rows from a nonexistent table returns an error."""
        result = runner.invoke(
            app, ["data-table-rows", "__nonexistent_table__", "column1,column2", "--api-key", API_TOKEN]
        )
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 500", result.output)

    def test_data_table_rows_outputs_json_representation_when_json_flag_is_true(self):
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "nimplex_composition_space",
                "Node_ID,NodeCoord_0,NodeCoord_1",
                "--api-key",
                API_TOKEN,
                "--json",
            ],
        )  # FIXME
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn("DataTableRow", result.output)

    def test_data_table_rows_empty_columns_for_rows(self):
        """Test that requesting rows with empty columns returns an error."""
        result = runner.invoke(app, ["data-table-rows", self.table_name, "", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("Missing required parameter", result.output)
        self.assertIn("columns", result.output)

    def test_data_table_rows_empty_columns_for_rows_json(self):
        """Test that requesting rows with empty columns returns an error."""
        result = runner.invoke(app, ["data-table-rows", self.table_name, "", "--api-key", API_TOKEN, "--json"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing required parameter", result.output)
        self.assertIn("columns", result.output)

    def test_help(self):
        """Test that the CLI help command works."""
        result = runner.invoke(app, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Datascribe CLI", result.output)

    def test_runs_cli_application_successfully(self):
        """Ensure the CLI application runs without errors."""
        result = runner.invoke(app, [])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("Missing command.", result.output)

    def test_displays_error_for_invalid_command(self):
        """Ensure an error is displayed for an invalid command."""
        result = runner.invoke(app, ["invalid-command"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("No such command", result.output)
