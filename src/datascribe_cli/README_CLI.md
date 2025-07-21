# `datascribe_cli`

Datascribe CLI - Interact with the DataScribe API.

**Usage**:

```console
$ datascribe_cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `data-tables`: This command retrieves and displays all...
* `data-table`: This command retrieves and displays a...
* `data-tables-for-user`: This command retrieves and displays all...
* `data-table-rows`: This command retrieves and displays rows...
* `data-table-columns`: This command retrieves and displays the...
* `data-table-metadata`: This command retrieves and displays...
* `data-table-rows-count`: This command retrieves and displays the...

---

## `datascribe_cli data-tables`

This command retrieves and displays all data tables available in the DataScribe API.

**Arguments**:

* `api_key` (str): Your DataScribe API key, which can also be set using the environment variable `DATASCRIBE_API_TOKEN`.

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--help`: Show this message and exit.
*
**Usage**:

```console
$ datascribe_cli data-tables [OPTIONS]
```

---

## `datascribe_cli data-table`

This command retrieves and displays a specific data table from the DataScribe API.

**Arguments**:

* `table_name` (str): The name of the data table to retrieve.
* `api_key` (str): Your DataScribe API key, which can also be set using the environment variable `DATASCRIBE_API_TOKEN`.

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--help`: Show this message and exit.
*
**Usage**:

```console
$ datascribe_cli data-table [OPTIONS] TABLE_NAME
```

## `datascribe_cli data-tables-for-user`

This command retrieves and displays all data tables that the authenticated user has access to in the DataScribe API.

**Arguments**:

* `api_key` (str): Your DataScribe API key, which can also be set using the environment variable `DATASCRIBE_API_TOKEN`.

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--help`: Show this message and exit.
*
**Usage**:

```console
$ datascribe_cli data-tables-for-user [OPTIONS]
```

---

## `datascribe_cli data-table-rows`

This command retrieves and displays rows from a specified data table, allowing you to specify which columns to include.

**Arguments**:

* `table_name` (str): The name of the data table to retrieve rows from.
* `columns` (str): A comma-separated list of column names to include in the output.
* `api_key` (str): Your DataScribe API key, which can also be set using the environment variable `DATASCRIBE_API_TOKEN`.

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--help`: Show this message and exit.

**Usage**:

```console
$ datascribe_cli data-table-rows [OPTIONS] TABLE_NAME COLUMNS
```

---

## `datascribe_cli data-table-columns`

This command retrieves and displays the columns of a specified data table in the DataScribe API.

**Arguments**:

* `table_name` (str): The name of the data table to retrieve columns from.
* `api_key` (str): Your DataScribe API key, which can also be set using the environment variable `DATASCRIBE_API_TOKEN`.

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--help`: Show this message and exit.
*
**Usage**:

```console
$ datascribe_cli data-table-columns [OPTIONS] TABLE_NAME
```

---

## `datascribe_cli data-table-metadata`

This command retrieves and displays metadata for a specified data table in the DataScribe API.

**Arguments**:

* `table_name` (str): The name of the data table to retrieve metadata for.
* `api_key` (str): Your DataScribe API key, which can also be set using the environment variable `DATASCRIBE_API_TOKEN`.

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--help`: Show this message and exit.

**Usage**:

```console
$ datascribe_cli data-table-metadata [OPTIONS] TABLE_NAME
```

---

## `datascribe_cli data-table-rows-count`

This command retrieves and displays the number of rows in a specified data table in the DataScribe API.

**Arguments**:

* `table_name` (str): The name of the data table to count rows in.
* `api_key` (str): Your DataScribe API key, which can also be set using the environment variable

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--help`: Show this message and exit.

**Usage**:

```console
$ datascribe_cli data-table-rows-count [OPTIONS] TABLE_NAME
```
