"""Datascribe CLI - A command-line interface for interacting with the DataScribe API."""

from typing import Annotated

import typer
from rich import print as pretty_print
from rich.panel import Panel

from datascribe_api import DataScribeClient

app = typer.Typer(help="Datascribe CLI - Interact with the DataScribe API.", pretty_exceptions_show_locals=False)


def handle_error(e: Exception):
    """Handle errors by printing them to the console.

    Args:
        e (Exception): The exception to handle.
    """
    pretty_print(Panel(renderable=f"{e}", title="Error", title_align="left", border_style="red"))


@app.command("data-tables")
def data_tables(
    api_key: Annotated[str, typer.Option(envvar="DATASCRIBE_API_TOKEN", show_default=False, help="Your DataScribe API key.")],
    json: Annotated[bool | None, typer.Option("--json", help="Output in JSON format.")] = None,
):
    """This command retrieves and displays all data tables available in the DataScribe API."""
    try:
        with DataScribeClient(api_key=api_key) as client:
            for table in client.get_data_tables():
                if json:
                    typer.echo(table.model_dump_json())
                else:
                    pretty_print(table)
    except Exception as e:
        handle_error(e)


@app.command("data-table")
def data_table(
    table_name: Annotated[str, typer.Argument(help="Name of the data table.", show_default=False)],
    api_key: Annotated[str, typer.Option(envvar="DATASCRIBE_API_TOKEN", show_default=False, help="Your DataScribe API key.")],
    starting_row: Annotated[int, typer.Option("--starting-row", "-s", help="Starting row index for pagination.")] = 0,
    num_rows: Annotated[int, typer.Option("--num-rows", "-n", help="Number of rows to retrieve.")] = 100,
    json: Annotated[bool | None, typer.Option("--json", help="Output in JSON format.")] = None,
):
    """This command retrieves and displays a specific data table from the DataScribe API."""
    try:
        with DataScribeClient(api_key=api_key) as client:
            table = client.get_data_table(tableName=table_name, startingRow=starting_row, numRows=num_rows)
            if json:
                typer.echo(table.model_dump_json())
            else:
                pretty_print(table)
    except Exception as e:
        handle_error(e)


@app.command("data-tables-for-user")
def data_tables_for_user(
    api_key: Annotated[str, typer.Option(envvar="DATASCRIBE_API_TOKEN", show_default=False, help="Your DataScribe API key.")],
    json: Annotated[bool | None, typer.Option("--json", help="Output in JSON format.")] = None,
):
    """This command retrieves and displays all data tables that the authenticated user has access to in the DataScribe API."""
    try:
        with DataScribeClient(api_key=api_key) as client:
            for table in client.get_data_tables_for_user():
                if json:
                    typer.echo(table.json())
                else:
                    pretty_print(table)
    except Exception as e:
        handle_error(e)


@app.command("data-table-rows")
def data_table_rows(
    table_name: Annotated[str, typer.Argument(help="Name of the data table.", show_default=False)],
    columns: Annotated[str, typer.Argument(help="Comma-separated list of columns.")],
    api_key: Annotated[str, typer.Option(envvar="DATASCRIBE_API_TOKEN", show_default=False, help="Your DataScribe API key.")],
    starting_row: Annotated[int, typer.Option("--starting-row", "-s", help="Starting row index for pagination.")] = 0,
    num_rows: Annotated[int, typer.Option("--num-rows", "-n", help="Number of rows to retrieve.")] = 100,
    json: Annotated[bool | None, typer.Option("--json", help="Output in JSON format.")] = None,
):
    """This command retrieves and displays rows from a specified data table, allowing you to specify which columns to include."""
    try:
        with DataScribeClient(api_key=api_key) as client:
            cols = columns.split(",")
            for row in client.get_data_table_rows(tableName=table_name, columns=cols, startingRow=starting_row, numRows=num_rows):
                if json:
                    typer.echo(row.model_dump_json())
                else:
                    pretty_print(row)
    except Exception as e:
        handle_error(e)


@app.command("data-table-columns")
def data_table_columns(
    table_name: Annotated[str, typer.Argument(help="Name of the data table.", show_default=False)],
    api_key: Annotated[str, typer.Option(envvar="DATASCRIBE_API_TOKEN", show_default=False, help="Your DataScribe API key.")],
    json: Annotated[bool | None, typer.Option("--json", help="Output in JSON format.")] = None,
):
    """This command retrieves and displays the columns of a specified data table in the DataScribe API."""
    try:
        with DataScribeClient(api_key=api_key) as client:
            columns = client.get_data_table_columns(tableName=table_name)
            if json:
                typer.echo(columns.model_dump_json())
            else:
                pretty_print(columns)
    except Exception as e:
        handle_error(e)


@app.command("data-table-metadata")
def data_table_metadata(
    table_name: Annotated[str, typer.Argument(help="Name of the data table.", show_default=False)],
    api_key: Annotated[str, typer.Option(envvar="DATASCRIBE_API_TOKEN", show_default=False, help="Your DataScribe API key.")],
    json: Annotated[bool | None, typer.Option("--json", help="Output in JSON format.")] = None,
):
    """This command retrieves and displays metadata for a specified data table in the DataScribe API."""
    try:
        with DataScribeClient(api_key=api_key) as client:
            metadata = client.get_data_table_metadata(tableName=table_name)
            if json:
                typer.echo(metadata.model_dump_json())
            else:
                pretty_print(metadata)
    except Exception as e:
        handle_error(e)


@app.command("data-table-rows-count")
def data_table_rows_count(
    table_name: Annotated[str, typer.Argument(help="Name of the data table.", show_default=False)],
    api_key: Annotated[str, typer.Option(envvar="DATASCRIBE_API_TOKEN", show_default=False, help="Your DataScribe API key.")],
    json: Annotated[bool | None, typer.Option("--json", help="Output in JSON format.")] = None,
):
    """This command retrieves and displays the number of rows in a specified data table in the DataScribe API."""
    try:
        with DataScribeClient(api_key=api_key) as client:
            count = client.get_data_table_rows_count(tableName=table_name)
            if json:
                typer.echo(count.model_dump_json())
            else:
                pretty_print(count)
    except Exception as e:
        handle_error(e)


@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    """Default command that displays the help message."""
    typer.echo(ctx.get_help())


if __name__ == "__main__":
    app(prog_name="datascribe-cli")
