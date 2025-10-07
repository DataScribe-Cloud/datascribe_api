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

---

## `datascribe_cli get-material-by-id`

Get material details by ID from selected providers.

**Usage**:

```console
$ datascribe_cli get-material-by-id [OPTIONS] IDS
```

**Arguments**:

* `IDS`: Material IDs to retrieve (e.g., mp-190, aflow:xxxx).  [required]

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--mp`: Query Materials Project provider.
* `--aflow`: Query AFLOW provider.
* `--json`: Output in JSON format.

---

## `datascribe_cli search-materials`

Search for materials using formula, elements, and other filters.

**Usage**:

```console
$ datascribe_cli search-materials [OPTIONS] FORMULA ELEMENTS EXCLUDE_ELEMENTS SPACEGROUP PROPS TEMPERATURE
```

**Arguments**:

* `FORMULA`: Chemical formula to search for (e.g., SiO2, Fe2O3).  [required]
* `ELEMENTS`: Comma-separated list of required elements (e.g., Si,O).  [required]
* `EXCLUDE_ELEMENTS`: Comma-separated list of elements to exclude (e.g., Pb,Hg).  [required]
* `SPACEGROUP`: Space group or crystal system to filter by (e.g., cubic, Pnma).  [required]
* `PROPS`: Comma-separated list of properties to include (e.g., band_gap,formation_energy).  [required]
* `TEMPERATURE`: Temperature filter (if supported by provider).  [required]

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--mp`: Query Materials Project provider.
* `--aflow`: Query AFLOW provider.
* `--page INTEGER`: Page number for paginated results.   [default: 1]
* `--size INTEGER`: Number of results per page.   [default: 50]
* `--json`: Output in JSON format.
