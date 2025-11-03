"""Testing suite for the CLI module.

This module contains unittests for the DataScribe Typer CLI commands.
It verifies correct behavior for data table retrieval, metadata, columns, rows, and error handling.
"""

import os
import subprocess
import sys

import pytest
from typer.testing import CliRunner

from datascribe_api import DataScribeClient
from datascribe_api.cli import app, parse_filter_string
from datascribe_api.filter import Filter

API_TOKEN: str | None = os.environ.get("DATASCRIBE_API_TOKEN")
ADMIN_API_TOKEN: str | None = os.environ.get("DATASCRIBE_ADMIN_API_TOKEN")
runner = CliRunner()


@pytest.mark.skipif(not API_TOKEN, reason="DATASCRIBE_API_TOKEN not set in environment")
class TestDataScribeCLI:
    """Unit tests for the DataScribe Typer CLI."""

    @classmethod
    def setup_class(cls):
        """Set up resources required for all tests in this class."""
        cls.client = DataScribeClient(api_key=API_TOKEN)
        tables = cls.client.get_data_tables_for_user()
        table_name: str | None = getattr(tables[-2], "table_name", None)
        columns = cls.client.get_data_table_columns(tableName=table_name)
        cls.table_name = table_name
        cls.columns = columns.to_list()

    @classmethod
    def teardown_class(cls):
        """Clean up resources initialized for all tests in this class."""
        cls.client.close()

    def test_script_runs_cli(self) -> None:
        """Test script runs CLI."""
        result = subprocess.run(
            ["datascribe_cli", "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "DataScribe CLI" in result.stdout
        assert "Usage:" in result.stdout

    def test_main_entry_point_runs_cli(self) -> None:
        """Test that running DataScribe Typer CLI as a module shows the CLI help."""
        result = subprocess.run(
            [sys.executable, "-m", "datascribe_api", "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "DataScribe CLI" in result.stdout
        assert "Usage:" in result.stdout

    @pytest.mark.skipif(not ADMIN_API_TOKEN, reason="DATASCRIBE_ADMIN_API_TOKEN not set in environment")
    def test_data_tables(self) -> None:
        """Test retrieving all data tables."""
        result = runner.invoke(app, ["data-tables", "--api-key", ADMIN_API_TOKEN])
        assert result.exit_code == 0
        assert "table_name" in result.output

    @pytest.mark.skipif(not ADMIN_API_TOKEN, reason="DATASCRIBE_ADMIN_API_TOKEN not set in environment")
    def test_data_tables_json(self) -> None:
        """Test retrieving all data tables with JSON output."""
        result = runner.invoke(app, ["data-tables", "--api-key", ADMIN_API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert "table_name" in result.output

    def test_data_tables_insufficient_permissions(self) -> None:
        """Test that insufficient permissions returns an error."""
        # This test assumes that the API token used does not have permission to access data tables.
        result = runner.invoke(app, ["data-tables", "--api-key", API_TOKEN])
        assert "Error" in result.output
        assert "Forbidden" in result.output
        assert "User is not a datascribe manager" in result.output

    def test_data_tables_for_user(self) -> None:
        """Test retrieving all data tables for the user."""
        result = runner.invoke(app, ["data-tables-for-user", "--api-key", API_TOKEN])
        assert result.exit_code == 0
        assert "table_name" in result.output

    def test_data_tables_for_user_invalid_api_key(self) -> None:
        """Test that an invalid API key returns an error."""
        result = runner.invoke(app, ["data-tables-for-user", "--api-key", "invalid_key"])
        assert "Error" in result.output
        assert "Unauthorized" in result.output
        assert "Invalid API key" in result.output

    def test_data_table(self) -> None:
        """Test retrieving a specific data table."""
        result = runner.invoke(app, ["data-table", "-t", self.table_name, "--api-key", API_TOKEN])
        assert result.exit_code == 0
        assert "DataTableRows" in result.output
        assert "DataTableRow" in result.output
        assert "_datascribe_user" in result.output
        assert "_datascribe_insert_time" in result.output
        assert "_datascribe_metadata" in result.output

    def test_data_table_missing_required_param(self) -> None:
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table"])
        assert "Error" in result.output
        assert "Missing option" in result.output

    def test_data_table_nonexistent_table(self) -> None:
        """Test that requesting a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table", "-t", "__nonexistent_table__", "--api-key", API_TOKEN])
        assert "Error" in result.output
        assert "HTTP Error 404" in result.output
        assert "Table not found" in result.output

    def test_data_table_outputs_json_representation_when_json_flag_is_true(self) -> None:
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(app, ["data-table", "-t", self.table_name, "--api-key", API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert "DataTableRows" not in result.output
        assert "DataTableRow" not in result.output

    def test_data_table_starting_row(self) -> None:
        """Test retrieving a specific data table with starting row."""
        result = runner.invoke(app, ["data-table", "-t", self.table_name, "--api-key", API_TOKEN, "--starting-row", "0"])
        assert result.exit_code == 0
        assert "DataTableRows" in result.output

    def test_data_table_starting_row_invalid(self) -> None:
        """Test that an invalid starting row returns an error."""
        result = runner.invoke(app, ["data-table", "-t", self.table_name, "--api-key", API_TOKEN, "--starting-row", "-1"])
        assert "Error" in result.output
        assert "HTTP Error 500" in result.output
        assert "OFFSET must not be negative" in result.output

    def test_data_table_starting_row_short_name(self) -> None:
        """Test retrieving a specific data table with starting row using short name."""
        result = runner.invoke(app, ["data-table", "-t", self.table_name, "--api-key", API_TOKEN, "-s", "0"])
        assert result.exit_code == 0
        assert "DataTableRows" in result.output

    def test_data_table_num_rows(self) -> None:
        """Test retrieving a specific data table with a specified number of rows."""
        result = runner.invoke(app, ["data-table", "-t", self.table_name, "--api-key", API_TOKEN, "--num-rows", "10"])
        assert result.exit_code == 0
        assert "DataTableRows" in result.output

    def test_data_table_num_rows_invalid(self) -> None:
        """Test that an invalid number of rows returns an error."""
        result = runner.invoke(app, ["data-table", "-t", self.table_name, "--api-key", API_TOKEN, "--num-rows", "-1"])
        assert "Error" in result.output
        assert "HTTP Error 500" in result.output
        assert "LIMIT must not be negative" in result.output

    def test_data_table_num_rows_short_name(self) -> None:
        """Test retrieving a specific data table with a specified number of rows using short name."""
        result = runner.invoke(app, ["data-table", "-t", self.table_name, "--api-key", API_TOKEN, "-n", "10"])
        assert result.exit_code == 0
        assert "DataTableRows" in result.output

    def test_data_table_columns(self) -> None:
        """Test retrieving columns for a data table."""
        result = runner.invoke(app, ["data-table-columns", "-t", self.table_name, "--api-key", API_TOKEN])
        assert result.exit_code == 0
        assert "DataTableColumns" in result.output
        assert "table_name" in result.output
        assert "display_name" in result.output
        assert "column_name" in result.output

    def test_data_table_columns_missing_required_param(self) -> None:
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table-columns"])
        assert "Error" in result.output
        assert "Missing option" in result.output

    def test_data_table_columns_nonexistent_table(self) -> None:
        """Test that requesting columns for a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table-columns", "-t", "__nonexistent_table__", "--api-key", API_TOKEN])
        assert "Error" in result.output
        assert "HTTP Error 404" in result.output
        assert "Table not found" in result.output

    def test_data_table_columns_outputs_json_representation_when_json_flag_is_true(self) -> None:
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(app, ["data-table-columns", "-t", self.table_name, "--api-key", API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert "DataTableColumns" not in result.output
        assert "table_name" in result.output
        assert "display_name" in result.output
        assert "column_name" in result.output

    def test_data_table_metadata(self) -> None:
        """Test retrieving metadata for a data table."""
        result = runner.invoke(app, ["data-table-metadata", "-t", self.table_name, "--api-key", API_TOKEN])
        assert result.exit_code == 0
        assert "DataTableMetadata" in result.output
        assert "table_name" in result.output
        assert "display_name" in result.output
        assert "user_id" in result.output
        assert "created_on" in result.output
        assert "last_updated" in result.output
        assert "table_type" in result.output
        assert "visibility" in result.output

    def test_data_table_metadata_missing_required_param(self) -> None:
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table-metadata"])
        assert "Error" in result.output
        assert "Missing option" in result.output

    def test_data_table_metadata_nonexistent_table(self) -> None:
        """Test that requesting metadata for a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table-metadata", "-t", "__nonexistent_table__", "--api-key", API_TOKEN])
        assert "Error" in result.output
        assert "HTTP Error 404" in result.output
        assert "Table not found" in result.output

    def test_data_table_metadata_outputs_json_representation_when_json_flag_is_true(self) -> None:
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(app, ["data-table-metadata", "-t", self.table_name, "--api-key", API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert "DataTableMetadata" not in result.output
        assert "table_name" in result.output
        assert "display_name" in result.output
        assert "user_id" in result.output
        assert "created_on" in result.output
        assert "last_updated" in result.output
        assert "table_type" in result.output
        assert "visibility" in result.output

    def test_data_table_rows_count(self) -> None:
        """Test retrieving the row count for a data table."""
        result = runner.invoke(app, ["data-table-rows-count", "-t", self.table_name, "--api-key", API_TOKEN])
        assert result.exit_code == 0
        assert "DataTableRowsCount" in result.output
        assert "total_rows" in result.output

    def test_data_table_rows_count_nonexistent_table(self) -> None:
        """Test that requesting row count for a nonexistent table returns an error."""
        result = runner.invoke(app, ["data-table-rows-count", "-t", "__nonexistent_table__", "--api-key", API_TOKEN])
        assert "Error" in result.output
        assert "HTTP Error 404" in result.output
        assert "Table not found" in result.output

    def test_data_table_rows_count_outputs_json_representation_when_json_flag_is_true(self) -> None:
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(app, ["data-table-rows-count", "-t", self.table_name, "--api-key", API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert "DataTableRowsCount" not in result.output
        assert "total_rows" in result.output

    def test_data_table_rows_count_missing_required_param(self) -> None:
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table-rows-count"])
        assert "Error" in result.output
        assert "Missing option" in result.output

    def test_data_table_rows(self) -> None:
        """Test retrieving rows from a data table."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
            ],
        )
        assert result.exit_code == 0
        assert "DataTableRow" in result.output

    def test_data_table_rows_missing_required_param(self) -> None:
        """Test that missing required parameters returns an error."""
        result = runner.invoke(app, ["data-table-rows"])
        assert "Error" in result.output
        assert "Missing option" in result.output

    def test_data_table_rows_nonexistent_table(self) -> None:
        """Test that requesting rows from a nonexistent table returns an error."""
        result = runner.invoke(
            app, ["data-table-rows", "-t", "__nonexistent_table__", "-c", "column1,column2", "--api-key", API_TOKEN]
        )
        assert "Error" in result.output
        assert "HTTP Error 404" in result.output
        assert "Table not found" in result.output

    def test_data_table_rows_outputs_json_representation_when_json_flag_is_true(self) -> None:
        """Ensure the command outputs JSON representation when the --json flag is set."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
                "--json",
            ],
        )
        assert result.exit_code == 0
        assert "DataTableRow" not in result.output

    def test_data_table_rows_empty_columns_for_rows(self) -> None:
        """Test that requesting rows with empty columns returns an error."""
        result = runner.invoke(app, ["data-table-rows", "-t", self.table_name, "-c", "", "--api-key", API_TOKEN])
        assert "Error" in result.output
        assert "Missing required parameter" in result.output
        assert "columns" in result.output

    def test_data_table_rows_empty_columns_for_rows_json(self) -> None:
        """Test that requesting rows with empty columns returns an error."""
        result = runner.invoke(app, ["data-table-rows", "-t", self.table_name, "-c", "", "--api-key", API_TOKEN, "--json"])
        assert "Error" in result.output
        assert "Missing required parameter" in result.output
        assert "columns" in result.output

    def test_data_table_rows_starting_row(self) -> None:
        """Test retrieving rows from a data table with a specified starting row."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
                "--starting-row",
                "0",
            ],
        )
        assert result.exit_code == 0
        assert "DataTableRow" in result.output

    def test_data_table_rows_starting_row_invalid(self) -> None:
        """Test that an invalid starting row returns an error."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
                "--starting-row",
                "-1",
            ],
        )
        assert "Error" in result.output
        assert "HTTP Error 400" in result.output
        assert "startingRow must be a valid non-negative integer" in result.output

    def test_data_table_rows_starting_row_short_name(self) -> None:
        """Test retrieving rows from a data table with a specified starting row using short name."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
                "-s",
                "0",
            ],
        )
        assert result.exit_code == 0
        assert "DataTableRow" in result.output

    def test_data_table_rows_num_rows(self) -> None:
        """Test retrieving rows from a data table with a specified number of rows."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
                "--num-rows",
                "10",
            ],
        )
        assert result.exit_code == 0
        assert "DataTableRow" in result.output

    def test_data_table_rows_num_rows_invalid(self) -> None:
        """Test that an invalid number of rows returns an error."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
                "--num-rows",
                "-1",
            ],
        )
        assert "Error" in result.output
        assert "HTTP Error 400" in result.output
        assert "numRows must be a valid positive integer" in result.output

    def test_data_table_rows_num_rows_short_name(self) -> None:
        """Test retrieving rows from a data table with a specified number of rows using short name."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
                "-n",
                "10",
            ],
        )
        assert result.exit_code == 0
        assert "DataTableRow" in result.output

    def test_help(self) -> None:
        """Test that the CLI help command works."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "DataScribe CLI" in result.output

    def test_runs_cli_application_successfully(self) -> None:
        """Ensure the CLI application runs without errors."""
        result = runner.invoke(app, [])
        assert result.exit_code == 2
        assert "DataScribe CLI" in result.output

    def test_shows_help_message_when_no_command_is_provided(self) -> None:
        """Ensure the help message is displayed when no command is provided."""
        result = runner.invoke(app, [])
        assert result.exit_code == 2
        assert "DataScribe CLI" in result.output
        assert "Usage:" in result.output
        assert "Options" in result.output
        assert "Commands" in result.output

    def test_displays_error_for_invalid_command(self) -> None:
        """Ensure an error is displayed for an invalid command."""
        result = runner.invoke(app, ["invalid-command"])
        assert result.exit_code != 0
        assert "No such command" in result.output

    def test_data_table_rows_with_basic_filter(self) -> None:
        """Test data-table-rows with a basic filter (col=value)."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
                "--filter",
                f"{self.columns[0]} is not null",
            ],
        )
        assert result.exit_code == 0
        assert "DataTableRow" in result.output

    def test_data_table_rows_with_multiple_filters(self) -> None:
        """Test data-table-rows with multiple filters (AND logic)."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
                "--filter",
                f"{self.columns[0]} is not null",
                "--filter",
                f"{self.columns[1]} is not null",
            ],
        )
        assert result.exit_code == 0
        assert "DataTableRow" in result.output

    def test_data_table_rows_with_in_filter(self) -> None:
        """Test data-table-rows with an IN filter."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
                "--filter",
                f"{self.columns[0]} in foo,bar,baz",
            ],
        )
        assert result.exit_code == 0

    def test_data_table_rows_with_like_filter(self) -> None:
        """Test data-table-rows with a LIKE filter."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
                "--filter",
                f"{self.columns[0]} like %a%",
            ],
        )
        assert result.exit_code == 0

    def test_data_table_rows_with_invalid_filter(self) -> None:
        """Test data-table-rows with an invalid filter syntax (should error)."""
        result = runner.invoke(
            app,
            [
                "data-table-rows",
                "-t",
                self.table_name,
                "-c",
                ",".join(map(str, self.columns[:3])),
                "--api-key",
                API_TOKEN,
                "--filter",
                "invalidfilter",
            ],
        )
        assert "Invalid filter syntax" in result.output

    def test_data_table_rows_count_with_filter(self) -> None:
        """Test data-table-rows-count with a filter."""
        result = runner.invoke(
            app,
            [
                "data-table-rows-count",
                "-t",
                self.table_name,
                "--api-key",
                API_TOKEN,
                "--filter",
                f"{self.columns[0]} is not null",
            ],
        )
        assert result.exit_code == 0
        assert "DataTableRowsCount" in result.output

    def test_is_null(self) -> None:
        """Test parse_filter_string with 'is null' operator."""
        f = parse_filter_string("foo is null")
        assert isinstance(f, Filter)
        assert f.to_dict()["operator"] == "is null"

    def test_is_not_null(self) -> None:
        """Test parse_filter_string with 'is not null' operator."""
        f = parse_filter_string("foo is not null")
        assert isinstance(f, Filter)
        assert f.to_dict()["operator"] == "is not null"

    def test_in(self) -> None:
        """Test parse_filter_string with 'in' operator."""
        f = parse_filter_string("bar in a,b,c")
        assert isinstance(f, Filter)
        assert f.to_dict()["operator"] == "in"

    def test_not_in(self) -> None:
        """Test parse_filter_string with 'not in' operator."""
        f = parse_filter_string("bar not in a,b,c")
        assert isinstance(f, Filter)
        assert f.to_dict()["operator"] == "not in"

    def test_like(self) -> None:
        """Test parse_filter_string with 'like' operator."""
        f = parse_filter_string("baz like %foo%")
        assert isinstance(f, Filter)
        assert f.to_dict()["operator"] == "like"

    def test_ilike(self) -> None:
        """Test parse_filter_string with 'ilike' operator."""
        f = parse_filter_string("baz ilike %foo%")
        assert isinstance(f, Filter)
        assert f.to_dict()["operator"] == "ilike"

    def test_eq(self) -> None:
        """Test parse_filter_string with '==' operator."""
        f = parse_filter_string("col==val")
        assert isinstance(f, Filter)
        assert f.to_dict()["operator"] == "="

    def test_ne(self) -> None:
        """Test parse_filter_string with '!=' operator."""
        f = parse_filter_string("col!=val")
        assert isinstance(f, Filter)
        assert f.to_dict()["operator"] == "!="

    def test_gt(self) -> None:
        """Test parse_filter_string with '>' operator."""
        f = parse_filter_string("col>5")
        assert isinstance(f, Filter)
        assert f.to_dict()["operator"] == ">"

    def test_ge(self) -> None:
        """Test parse_filter_string with '>=' operator."""
        f = parse_filter_string("col>=5")
        assert isinstance(f, Filter)
        assert f.to_dict()["operator"] == ">="

    def test_lt(self) -> None:
        """Test parse_filter_string with '<' operator."""
        f = parse_filter_string("col<5")
        assert isinstance(f, Filter)
        assert f.to_dict()["operator"] == "<"

    def test_le(self) -> None:
        """Test parse_filter_string with '<=' operator."""
        f = parse_filter_string("col<=5")
        assert isinstance(f, Filter)
        assert f.to_dict()["operator"] == "<="

    def test_get_material_by_id_mp(self) -> None:
        """Test get_material_by_id with a valid MP material ID and --mp flag."""
        mp_id = "mp-149"
        result = runner.invoke(app, ["get-material-by-id", "-i", mp_id, "--mp", "--api-key", API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert "provider" in result.output
        assert "data" in result.output
        assert "mp-149" in result.output

    def test_get_material_by_id_aflow(self) -> None:
        """Test get_material_by_id with a valid AFLOW material ID and --aflow flag."""
        aflow_id = "aflow:08ab41c5f54850db"
        result = runner.invoke(app, ["get-material-by-id", "-i", aflow_id, "--aflow", "--api-key", API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert "provider" in result.output
        assert "data" in result.output
        assert "aflow" in result.output

    def test_get_material_by_id_invalid(self) -> None:
        """Test get_material_by_id with an invalid material ID."""
        mp_id = "mp-invalid"
        result = runner.invoke(app, ["get-material-by-id", "-i", mp_id, "--mp", "--api-key", API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert "results" in result.output
        assert '"total":0' in result.output
        assert '"data": {' not in result.output

    def test_search_materials_mp(self) -> None:
        """Test search_materials with a valid formula and elements."""
        result = runner.invoke(app, ["search-materials", "-f", "SiO2", "-e", "Si,O", "--mp", "--api-key", API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert "results" in result.output
        assert "SiO2" in result.output

    def test_search_materials_aflow(self) -> None:
        """Test search_materials with a valid formula and elements."""
        result = runner.invoke(app, ["search-materials", "-e", "Si,O", "--aflow", "--api-key", API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert "results" in result.output
        assert "Si" in result.output
        assert "O" in result.output

    def test_search_materials_with_props(self) -> None:
        """Test search_materials with property filters."""
        result = runner.invoke(
            app, ["search-materials", "-f", "SiO2", "-e", "Si,O", "-p", "band_gap", "--mp", "--api-key", API_TOKEN, "--json"]
        )
        assert result.exit_code == 0
        assert "results" in result.output
        assert "SiO2" in result.output
        assert "bandgap" in result.output

    def test_search_materials_pagination(self) -> None:
        """Test search_materials with pagination options."""
        result = runner.invoke(
            app,
            [
                "search-materials",
                "-f",
                "SiO2",
                "-e",
                "Si,O",
                "--mp",
                "--api-key",
                API_TOKEN,
                "--json",
                "--page",
                "1",
                "--size",
                "2",
            ],
        )
        assert result.exit_code == 0
        assert "SiO2" in result.output
        assert "results" in result.output

    def test_search_materials_invalid_mp(self) -> None:
        """Test search_materials with empty input."""
        result = runner.invoke(app, ["search-materials", "-f", "mp-invalid", "--mp", "--api-key", API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert '"results":[]' in result.output

    def test_search_materials_invalid_aflow(self) -> None:
        """Test search_materials with empty input."""
        result = runner.invoke(app, ["search-materials", "-f", "aflow-invalid", "--aflow", "--api-key", API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert '"results":[]' in result.output

    def test_search_materials_json_output(self) -> None:
        """Test search_materials with JSON output flag."""
        result = runner.invoke(
            app,
            [
                "search-materials",
                "-f",
                "SiO2",
                "-e",
                "Si,O",
                "--mp",
                "--api-key",
                API_TOKEN,
                "--json",
            ],
        )
        assert result.exit_code == 0
        assert "SiO2" in result.output
        assert "results" in result.output

    def test_search_materials_cli_with_oqmd(self):
        """Test CLI search-materials command with --oqmd option."""
        result = runner.invoke(app, ["search-materials", "-f", "Al2O3", "--oqmd", "--api-key", API_TOKEN, "--json"])
        assert result.exit_code == 0
        assert "results" in result.output
        assert "Al2O3" in result.output
        assert "OQMD" in result.output
