# `datascribe_cli`

DataScribe CLI - Interact with the DataScribe API.

**Usage**:

```console
$ datascribe_cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.

**Commands**:

* `data-tables`: This command retrieves and displays all data tables available in the DataScribe API.
* `data-table`: This command retrieves and displays a specific data table from the DataScribe API.
* `data-tables-for-user`: This command retrieves and displays all data tables that the authenticated user has access to in the DataScribe API.
* `data-table-rows`: This command retrieves and displays rows from a specified data table, allowing you to specify which columns to include.
* `data-table-columns`: This command retrieves and displays the columns of a specified data table in the DataScribe API.
* `data-table-metadata`: This command retrieves and displays metadata for a specified data table in the DataScribe API.
* `data-table-rows-count`: This command retrieves and displays the number of rows in a specified data table in the DataScribe API.

---

## `datascribe_cli data-tables`

This command retrieves and displays all data tables available in the DataScribe API.

**Usage**:

```console
$ datascribe_cli data-tables [OPTIONS]
```

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--json`: Output in JSON format.

---

## `datascribe_cli data-table`

This command retrieves and displays a specific data table from the DataScribe API.

**Usage**:

```console
$ datascribe_cli data-table [OPTIONS] TABLE_NAME
```

**Arguments**:

* `TABLE_NAME`: Name of the data table.  [required]

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `-s, --starting-row INTEGER`: Starting row index for pagination.  [default: 0]
* `-n, --num-rows INTEGER`: Number of rows to retrieve.  [default: 100]
* `--json`: Output in JSON format.

## `datascribe_cli data-tables-for-user`

This command retrieves and displays all data tables that the authenticated user has access to in the DataScribe API.

**Usage**:

```console
$ datascribe_cli data-tables-for-user [OPTIONS]
```

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--json`: Output in JSON format.

---

## `datascribe_cli data-table-rows`

This command retrieves and displays rows from a specified data table, allowing you to specify which columns to include.

**Usage**:

```console
$ datascribe_cli data-table-rows [OPTIONS] TABLE_NAME COLUMNS
```

**Arguments**:

* `TABLE_NAME`: Name of the data table.  [required]
* `COLUMNS`: Comma-separated list of columns.  [required]

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `-s, --starting-row INTEGER`: Starting row index for pagination.  [default: 0]
* `-n, --num-rows INTEGER`: Number of rows to retrieve.  [default: 100]
* `--filter TEXT`: Filter expression. Can be used multiple times.
* `--json`: Output in JSON format.

---

## `datascribe_cli data-table-columns`

This command retrieves and displays the columns of a specified data table in the DataScribe API.

**Usage**:

```console
$ datascribe_cli data-table-columns [OPTIONS] TABLE_NAME
```

**Arguments**:

* `TABLE_NAME`: Name of the data table.  [required]

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--json`: Output in JSON format.

---

## `datascribe_cli data-table-metadata`

This command retrieves and displays metadata for a specified data table in the DataScribe API.

**Usage**:

```console
$ datascribe_cli data-table-metadata [OPTIONS] TABLE_NAME
```

**Arguments**:

* `TABLE_NAME`: Name of the data table.  [required]

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--json`: Output in JSON format.

---

## `datascribe_cli data-table-rows-count`

This command retrieves and displays the number of rows in a specified data table in the DataScribe API.

**Usage**:

```console
$ datascribe_cli data-table-rows-count [OPTIONS] TABLE_NAME
```

**Arguments**:

* `TABLE_NAME`: Name of the data table.  [required]

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--filter TEXT`: Filter expression. Can be used multiple times.
* `--json`: Output in JSON format.
