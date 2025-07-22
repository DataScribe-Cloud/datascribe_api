"""Datascribe CLI - A command-line interface for interacting with the DataScribe API."""

import typer
from rich import print as pretty_print

from datascribe_api import DataScribeClient

app = typer.Typer(help="Datascribe CLI - Interact with the DataScribe API.")


def handle_error(e: Exception):
    """Handle errors by printing them to the console.

    Args:
        e (Exception): The exception to handle.
    """
    typer.secho(f"Error: {e}", err=True, fg=typer.colors.RED)


@app.command("data-tables")
def data_tables(
    json: bool = typer.Option(False, "--json", help="Output in JSON format."),
    api_key: str = typer.Option(..., "--api-key", envvar="DATASCRIBE_API_TOKEN", help="Your DataScribe API key."),
):
    """This command retrieves and displays all data tables available in the DataScribe API.

    Args:
        json (bool): If set to True, the output will be formatted as JSON strings.
        api_key (str): Your DataScribe API key, which can also be set using the environment variable `DATASCRIBE_API_TOKEN`.
    """
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
    table_name: str = typer.Argument(..., help="Name of the data table."),
    json: bool = typer.Option(False, "--json", help="Output in JSON format."),
    api_key: str = typer.Option(..., "--api-key", envvar="DATASCRIBE_API_TOKEN", help="Your DataScribe API key."),
):
    """This command retrieves and displays a specific data table from the DataScribe API.

    Args:
        table_name (str): The name of the data table to retrieve.
        json (bool): If set to True, the output will be formatted as JSON strings.
        api_key (str): Your DataScribe API key, which can also be set using the environment variable `DATASCRIBE_API_TOKEN`.
    """
    try:
        with DataScribeClient(api_key=api_key) as client:
            table = client.get_data_table(tableName=table_name)
            if json:
                typer.echo(table.model_dump_json())
            else:
                pretty_print(table)
    except Exception as e:
        handle_error(e)


@app.command("data-tables-for-user")
def data_tables_for_user(
    api_key: str = typer.Option(..., "--api-key", envvar="DATASCRIBE_API_TOKEN", help="Your DataScribe API key."),
    json: bool = typer.Option(False, "--json", help="Output in JSON format."),
):
    """This command retrieves and displays all data tables that the authenticated user has access to in the DataScribe API.

    Args:
        api_key (str): Your DataScribe API key, which can also be set using the environment variable `DATASCRIBE_API_TOKEN`.
        json (bool): If set to True, the output will be formatted as JSON strings.
    """
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
    table_name: str = typer.Argument(..., help="Name of the data table."),
    columns: str = typer.Argument(..., help="Comma-separated list of columns."),
    json: bool = typer.Option(False, "--json", help="Output in JSON format."),
    api_key: str = typer.Option(..., "--api-key", envvar="DATASCRIBE_API_TOKEN", help="Your DataScribe API key."),
):
    """This command retrieves and displays rows from a specified data table, allowing you to specify which columns to include.

    Args:
        table_name (str): The name of the data table to retrieve rows from.
        columns (str): A comma-separated list of column names to include in the output.
        json (bool): If set to True, the output will be formatted as JSON strings.
        api_key (str): Your DataScribe API key, which can also be set using the environment variable `DATASCRIBE_API_TOKEN`.
    """
    try:
        with DataScribeClient(api_key=api_key) as client:
            cols = columns.split(",")
            rows = client.get_data_table_rows(tableName=table_name, columns=cols)
            for row in rows:
                if json:
                    typer.echo(row.model_dump_json())
                else:
                    pretty_print(row)
    except Exception as e:
        handle_error(e)


@app.command("data-table-columns")
def data_table_columns(
    table_name: str = typer.Argument(..., help="Name of the data table."),
    json: bool = typer.Option(False, "--json", help="Output in JSON format."),
    api_key: str = typer.Option(..., "--api-key", envvar="DATASCRIBE_API_TOKEN", help="Your DataScribe API key."),
):
    """This command retrieves and displays the columns of a specified data table in the DataScribe API.

    Args:
        table_name (str): The name of the data table to retrieve columns from.
        json (bool): If set to True, the output will be formatted as JSON strings.
        api_key (str): Your DataScribe API key, which can also be set using the environment variable `DATASCRIBE_API_TOKEN`.
    """
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
    table_name: str = typer.Argument(..., help="Name of the data table."),
    json: bool = typer.Option(False, "--json", help="Output in JSON format."),
    api_key: str = typer.Option(..., "--api-key", envvar="DATASCRIBE_API_TOKEN", help="Your DataScribe API key."),
):
    """This command retrieves and displays metadata for a specified data table in the DataScribe API.

    Args:
        table_name (str): The name of the data table to retrieve metadata for.
        json (bool): If set to True, the output will be formatted as JSON strings.
        api_key (str): Your DataScribe API key, which can also be set using the environment variable `DATASCRIBE_API_TOKEN`.
    """
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
    table_name: str = typer.Argument(..., help="Name of the data table."),
    json: bool = typer.Option(False, "--json", help="Output in JSON format."),
    api_key: str = typer.Option(..., "--api-key", envvar="DATASCRIBE_API_TOKEN", help="Your DataScribe API key."),
):
    """This command retrieves and displays the number of rows in a specified data table in the DataScribe API.

    Args:
        table_name (str): The name of the data table to count rows in.
        json (bool): If set to True, the output will be formatted as JSON strings.
        api_key (str): Your DataScribe API key, which can also be set using the environment variable
    """
    try:
        with DataScribeClient(api_key=api_key) as client:
            count = client.get_data_table_rows_count(tableName=table_name)
            if json:
                typer.echo(count.model_dump_json())
            else:
                pretty_print(count)
    except Exception as e:
        handle_error(e)


if __name__ == "__main__":
    app()
