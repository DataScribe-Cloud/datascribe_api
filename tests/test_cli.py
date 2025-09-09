"""Testing suite for the CLI module.

This module contains unittests for the datascribe_cli Typer CLI commands.
It verifies correct behavior for data table retrieval, metadata, columns, rows, and error handling.
"""

import json
import os
import re
import subprocess
import unittest

from typer.testing import CliRunner

from datascribe_api.filter import Filter
from datascribe_cli.cli import app, parse_filter_string

API_TOKEN: str | None = os.environ.get("DATASCRIBE_API_TOKEN")
ADMIN_API_TOKEN: str | None = os.environ.get("DATASCRIBE_ADMIN_API_TOKEN")
runner = CliRunner()


@unittest.skipUnless(API_TOKEN, "DATASCRIBE_API_TOKEN not set in environment")
class TestDataScribeCLI(unittest.TestCase):
    """Unit tests for the datascribe_cli Typer CLI."""

    def setUp(self) -> None:
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

    def test_script_runs_cli(self):
        """Test script runs CLI."""
        result = subprocess.run(
            ["datascribe_cli", "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Datascribe CLI", result.stdout)
        self.assertIn("Usage:", result.stdout)

    def test_main_entry_point_runs_cli(self):
        """Test that running datascribe_cli as a module shows the CLI help."""
        result = subprocess.run(
            ["python", "-m", "datascribe_cli", "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Datascribe CLI", result.stdout)
        self.assertIn("Usage:", result.stdout)

    @unittest.skipUnless(ADMIN_API_TOKEN, "DATASCRIBE_ADMIN_API_TOKEN not set in environment")
    def test_data_tables(self) -> None:
        """Test retrieving all data tables."""
        result = runner.invoke(app, ["data-tables", "--api-key", ADMIN_API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("table_name", result.output)

    @unittest.skipUnless(ADMIN_API_TOKEN, "DATASCRIBE_ADMIN_API_TOKEN not set in environment")
    def test_data_tables_json(self) -> None:
        """Test retrieving all data tables with JSON output."""
        result = runner.invoke(app, ["data-tables", "--api-key", ADMIN_API_TOKEN, "--json"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("table_name", result.output)

    def test_data_tables_insufficient_permissions(self) -> None:
        """Test that insufficient permissions returns an error."""
        # This test assumes that the API token used does not have permission to access data tables.
        result = runner.invoke(app, ["data-tables", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("Forbidden", result.output)
        self.assertIn("User is not a datascribe manager", result.output)

    def test_data_tables_for_user(self) -> None:
        """Test retrieving all data tables for the user."""
        result = runner.invoke(app, ["data-tables-for-user", "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("table_name", result.output)

    def test_data_tables_for_user_invalid_api_key(self) -> None:
        """Test that an invalid API key returns an error."""
        result = runner.invoke(app, ["data-tables-for-user", "--api-key", "invalid_key"])
        self.assertIn("Error", result.output)
        self.assertIn("Unauthorized", result.output)
        self.assertIn("Invalid API key", result.output)

    def test_data_table(self) -> None:
        """Test retrieving a specific data table."""
        result = runner.invoke(app, ["data-table", self.table_name, "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRows", result.output)
        self.assertIn("DataTableRow", result.output)
        self.assertIn("_datascribe_user", result.output)
        self.assertIn("_datascribe_insert_time", result.output)
        self.assertIn("_datascribe_metadata", result.output)

    def test_data_table_missing_required_param(self) -> None:
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing argument", result.output)

    def test_data_table_nonexistent_table(self) -> None:
        """Test that requesting a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table", "__nonexistent_table__", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 404", result.output)
        self.assertIn("Table not found", result.output)

    def test_data_table_outputs_json_representation_when_json_flag_is_true(self) -> None:
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(app, ["data-table", self.table_name, "--api-key", API_TOKEN, "--json"])
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn("DataTableRows", result.output)
        self.assertNotIn("DataTableRow", result.output)

    def test_data_table_starting_row(self) -> None:
        """Test retrieving a specific data table with starting row."""
        result = runner.invoke(app, ["data-table", self.table_name, "--api-key", API_TOKEN, "--starting-row", "0"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRows", result.output)

    def test_data_table_starting_row_invalid(self) -> None:
        """Test that an invalid starting row returns an error."""
        result = runner.invoke(app, ["data-table", self.table_name, "--api-key", API_TOKEN, "--starting-row", "-1"])
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 500", result.output)
        self.assertIn("OFFSET must not be negative", result.output)

    def test_data_table_starting_row_short_name(self) -> None:
        """Test retrieving a specific data table with starting row using short name."""
        result = runner.invoke(app, ["data-table", self.table_name, "--api-key", API_TOKEN, "-s", "0"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRows", result.output)

    def test_data_table_num_rows(self) -> None:
        """Test retrieving a specific data table with a specified number of rows."""
        result = runner.invoke(app, ["data-table", self.table_name, "--api-key", API_TOKEN, "--num-rows", "10"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRows", result.output)

    def test_data_table_num_rows_invalid(self) -> None:
        """Test that an invalid number of rows returns an error."""
        result = runner.invoke(app, ["data-table", self.table_name, "--api-key", API_TOKEN, "--num-rows", "-1"])
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 500", result.output)
        self.assertIn("LIMIT must not be negative", result.output)

    def test_data_table_num_rows_short_name(self) -> None:
        """Test retrieving a specific data table with a specified number of rows using short name."""
        result = runner.invoke(app, ["data-table", self.table_name, "--api-key", API_TOKEN, "-n", "10"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRows", result.output)

    def test_data_table_columns(self) -> None:
        """Test retrieving columns for a data table."""
        result = runner.invoke(app, ["data-table-columns", self.table_name, "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableColumns", result.output)
        self.assertIn("table_name", result.output)
        self.assertIn("display_name", result.output)
        self.assertIn("column_name", result.output)

    def test_data_table_columns_missing_required_param(self) -> None:
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table-columns"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing argument", result.output)

    def test_data_table_columns_nonexistent_table(self) -> None:
        """Test that requesting columns for a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table-columns", "__nonexistent_table__", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 404", result.output)
        self.assertIn("Table not found", result.output)

    def test_data_table_columns_outputs_json_representation_when_json_flag_is_true(self) -> None:
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(app, ["data-table-columns", self.table_name, "--api-key", API_TOKEN, "--json"])
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn("DataTableColumns", result.output)
        self.assertIn("table_name", result.output)
        self.assertIn("display_name", result.output)
        self.assertIn("column_name", result.output)

    def test_data_table_metadata(self) -> None:
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

    def test_data_table_metadata_missing_required_param(self) -> None:
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table-metadata"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing argument", result.output)

    def test_data_table_metadata_nonexistent_table(self) -> None:
        """Test that requesting metadata for a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table-metadata", "__nonexistent_table__", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 404", result.output)
        self.assertIn("Table not found", result.output)

    def test_data_table_metadata_outputs_json_representation_when_json_flag_is_true(self) -> None:
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

    def test_data_table_rows_count(self) -> None:
        """Test retrieving the row count for a data table."""
        result = runner.invoke(app, ["data-table-rows-count", self.table_name, "--api-key", API_TOKEN])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRowsCount", result.output)
        self.assertIn("total_rows", result.output)

    def test_data_table_rows_count_nonexistent_table(self) -> None:
        """Test that requesting row count for a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table-rows-count", "__nonexistent_table__", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 404", result.output)
        self.assertIn("Table not found", result.output)

    def test_data_table_rows_count_outputs_json_representation_when_json_flag_is_true(self) -> None:
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(app, ["data-table-rows-count", self.table_name, "--api-key", API_TOKEN, "--json"])
        self.assertEqual(result.exit_code, 0)
        self.assertNotIn("DataTableRowsCount", result.output)
        self.assertIn("total_rows", result.output)

    def test_data_table_rows_count_missing_required_param(self) -> None:
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table-rows-count"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing argument", result.output)

    def test_data_table_rows(self) -> None:
        """Test retrieving rows from a data table."""
        result = runner.invoke(
            app,
            ["data-table-rows", "nimplex_composition_space", "Node_ID,NodeCoord_0,NodeCoord_1", "--api-key", API_TOKEN],
        )  # FIXME
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRow", result.stdout)

    def test_data_table_rows_missing_required_param(self) -> None:
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table-rows"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing argument", result.output)

    def test_data_table_rows_nonexistent_table(self) -> None:
        """Test that requesting rows from a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table-rows", "__nonexistent_table__", "column1,column2", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 404", result.output)
        self.assertIn("Table not found", result.output)

    def test_data_table_rows_outputs_json_representation_when_json_flag_is_true(self) -> None:
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

    def test_data_table_rows_empty_columns_for_rows(self) -> None:
        """Test that requesting rows with empty columns returns an error."""
        result = runner.invoke(app, ["data-table-rows", self.table_name, "", "--api-key", API_TOKEN])
        self.assertIn("Error", result.output)
        self.assertIn("Missing required parameter", result.output)
        self.assertIn("columns", result.output)

    def test_data_table_rows_empty_columns_for_rows_json(self) -> None:
        """Test that requesting rows with empty columns returns an error."""
        result = runner.invoke(app, ["data-table-rows", self.table_name, "", "--api-key", API_TOKEN, "--json"])
        self.assertIn("Error", result.output)
        self.assertIn("Missing required parameter", result.output)
        self.assertIn("columns", result.output)

    def test_data_table_rows_starting_row(self) -> None:
        """Test retrieving rows from a data table with a specified starting row."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "nimplex_composition_space",
                "Node_ID,NodeCoord_0,NodeCoord_1",
                "--api-key",
                API_TOKEN,
                "--starting-row",
                "0",
            ],
        )  # FIXME
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRow", result.stdout)

    def test_data_table_rows_starting_row_invalid(self) -> None:
        """Test that an invalid starting row returns an error."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "nimplex_composition_space",
                "Node_ID,NodeCoord_0,NodeCoord_1",
                "--api-key",
                API_TOKEN,
                "--starting-row",
                "-1",
            ],
        )  # FIXME
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 400", result.output)
        self.assertIn("startingRow must be a valid non-negative integer", result.output)

    def test_data_table_rows_starting_row_short_name(self) -> None:
        """Test retrieving rows from a data table with a specified starting row using short name."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "nimplex_composition_space",
                "Node_ID,NodeCoord_0,NodeCoord_1",
                "--api-key",
                API_TOKEN,
                "-s",
                "0",
            ],
        )  # FIXME
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRow", result.stdout)

    def test_data_table_rows_num_rows(self) -> None:
        """Test retrieving rows from a data table with a specified number of rows."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "nimplex_composition_space",
                "Node_ID,NodeCoord_0,NodeCoord_1",
                "--api-key",
                API_TOKEN,
                "--num-rows",
                "10",
            ],
        )  # FIXME
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRow", result.stdout)

    def test_data_table_rows_num_rows_invalid(self) -> None:
        """Test that an invalid number of rows returns an error."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "nimplex_composition_space",
                "Node_ID,NodeCoord_0,NodeCoord_1",
                "--api-key",
                API_TOKEN,
                "--num-rows",
                "-1",
            ],
        )  # FIXME
        self.assertIn("Error", result.output)
        self.assertIn("HTTP Error 400", result.output)
        self.assertIn("numRows must be a valid positive integer", result.output)

    def test_data_table_rows_num_rows_short_name(self) -> None:
        """Test retrieving rows from a data table with a specified number of rows using short name."""
        result = runner.invoke(  # FIXME
            app,
            [
                "data-table-rows",
                "nimplex_composition_space",
                "Node_ID,NodeCoord_0,NodeCoord_1",
                "--api-key",
                API_TOKEN,
                "-n",
                "10",
            ],
        )  # FIXME
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRow", result.stdout)

    def test_help(self) -> None:
        """Test that the CLI help command works."""
        result = runner.invoke(app, ["--help"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Datascribe CLI", result.output)

    def test_runs_cli_application_successfully(self) -> None:
        """Ensure the CLI application runs without errors."""
        result = runner.invoke(app, [])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Datascribe CLI", result.output)

    def test_shows_help_message_when_no_command_is_provided(self) -> None:
        """Ensure the help message is displayed when no command is provided."""
        result = runner.invoke(app, [])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Datascribe CLI", result.output)
        self.assertIn("Usage:", result.output)
        self.assertIn("Options", result.output)
        self.assertIn("Commands", result.output)

    def test_displays_error_for_invalid_command(self) -> None:
        """Ensure an error is displayed for an invalid command."""
        result = runner.invoke(app, ["invalid-command"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("No such command", result.output)

    def test_data_table_rows_with_basic_filter(self) -> None:
        """Test data-table-rows with a basic filter (col=value)."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "nimplex_composition_space",
                "Node_ID,NodeCoord_0,NodeCoord_1",
                "--api-key",
                API_TOKEN,
                "--filter",
                "Node_ID is not null",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRow", result.stdout)

    def test_data_table_rows_with_multiple_filters(self) -> None:
        """Test data-table-rows with multiple filters (AND logic)."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "nimplex_composition_space",
                "Node_ID,NodeCoord_0,NodeCoord_1",
                "--api-key",
                API_TOKEN,
                "--filter",
                "Node_ID is not null",
                "--filter",
                "NodeCoord_0 is not null",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRow", result.stdout)

    def test_data_table_rows_with_in_filter(self) -> None:
        """Test data-table-rows with an IN filter."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "nimplex_composition_space",
                "Node_ID,NodeCoord_0,NodeCoord_1",
                "--api-key",
                API_TOKEN,
                "--filter",
                "Node_ID in foo,bar,baz",
            ],
        )
        self.assertEqual(result.exit_code, 0)

    def test_data_table_rows_with_like_filter(self) -> None:
        """Test data-table-rows with a LIKE filter."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "nimplex_composition_space",
                "Node_ID,NodeCoord_0,NodeCoord_1",
                "--api-key",
                API_TOKEN,
                "--filter",
                "Node_ID like %a%",
            ],
        )
        self.assertEqual(result.exit_code, 0)

    def test_data_table_rows_with_invalid_filter(self) -> None:
        """Test data-table-rows with an invalid filter syntax (should error)."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                self.table_name,
                self.columns_arg,
                "--api-key",
                API_TOKEN,
                "--filter",
                "invalidfilter",
            ],
        )
        self.assertIn("Invalid filter syntax", result.stdout)

    def test_data_table_rows_count_with_filter(self) -> None:
        """Test data-table-rows-count with a filter."""
        col1 = self.columns_arg.split(",")[0]
        result = runner.invoke(
            app,
            [
                "data-table-rows-count",
                self.table_name,
                "--api-key",
                API_TOKEN,
                "--filter",
                f"{col1} is not null",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("DataTableRowsCount", result.stdout)

    def test_is_null(self):
        """Test parse_filter_string with 'is null' operator."""
        f = parse_filter_string("foo is null")
        self.assertIsInstance(f, Filter)
        self.assertEqual(f.to_dict()["operator"], "is null")

    def test_is_not_null(self):
        """Test parse_filter_string with 'is not null' operator."""
        f = parse_filter_string("foo is not null")
        self.assertIsInstance(f, Filter)
        self.assertEqual(f.to_dict()["operator"], "is not null")

    def test_in(self):
        """Test parse_filter_string with 'in' operator."""
        f = parse_filter_string("bar in a,b,c")
        self.assertIsInstance(f, Filter)
        self.assertEqual(f.to_dict()["operator"], "in")

    def test_not_in(self):
        """Test parse_filter_string with 'not in' operator."""
        f = parse_filter_string("bar not in a,b,c")
        self.assertIsInstance(f, Filter)
        self.assertEqual(f.to_dict()["operator"], "not in")

    def test_like(self):
        """Test parse_filter_string with 'like' operator."""
        f = parse_filter_string("baz like %foo%")
        self.assertIsInstance(f, Filter)
        self.assertEqual(f.to_dict()["operator"], "like")

    def test_ilike(self):
        """Test parse_filter_string with 'ilike' operator."""
        f = parse_filter_string("baz ilike %foo%")
        self.assertIsInstance(f, Filter)
        self.assertEqual(f.to_dict()["operator"], "ilike")

    def test_eq(self):
        """Test parse_filter_string with '==' operator."""
        f = parse_filter_string("col==val")
        self.assertIsInstance(f, Filter)
        self.assertEqual(f.to_dict()["operator"], "=")

    def test_ne(self):
        """Test parse_filter_string with '!=' operator."""
        f = parse_filter_string("col!=val")
        self.assertIsInstance(f, Filter)
        self.assertEqual(f.to_dict()["operator"], "!=")

    def test_gt(self):
        """Test parse_filter_string with '>' operator."""
        f = parse_filter_string("col>5")
        self.assertIsInstance(f, Filter)
        self.assertEqual(f.to_dict()["operator"], ">")

    def test_ge(self):
        """Test parse_filter_string with '>=' operator."""
        f = parse_filter_string("col>=5")
        self.assertIsInstance(f, Filter)
        self.assertEqual(f.to_dict()["operator"], ">=")

    def test_lt(self):
        """Test parse_filter_string with '<' operator."""
        f = parse_filter_string("col<5")
        self.assertIsInstance(f, Filter)
        self.assertEqual(f.to_dict()["operator"], "<")

    def test_le(self):
        """Test parse_filter_string with '<=' operator."""
        f = parse_filter_string("col<=5")
        self.assertIsInstance(f, Filter)
        self.assertEqual(f.to_dict()["operator"], "<=")
