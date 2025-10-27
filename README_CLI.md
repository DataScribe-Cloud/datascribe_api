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

* `data-tables`: Retrieve and display all available data tables.
* `data-table`: Retrieve and display a specific data table.
* `data-tables-for-user`: Retrieve and display all data tables that the authenticated user has access to.
* `data-table-rows`: Retrieve and display rows from a specified data table, allowing you to specify which columns to include.
* `data-table-columns`: Retrieve and display the columns of a specified data table.
* `data-table-metadata`: Retrieve and display metadata for a specified data table.
* `data-table-rows-count`: Retrieve and display the number of rows in a specified data table.
* `get-material-by-id`: Get material details by ID from selected providers.
* `search-materials`: Search for materials using formula, elements, and other filters.

---

## `datascribe_cli data-tables`

Retrieve and display all available data tables.

**Usage**:

```console
$ datascribe_cli data-tables [OPTIONS]
```

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--json`: Output in JSON format.

---

## `datascribe_cli data-table`

Retrieve and display a specific data table.

**Usage**:

```console
$ datascribe_cli data-table [OPTIONS]
```

**Options**:

* `-t, --table-name TEXT`: Name of the data table.  [required]
* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `-s, --starting-row INTEGER`: Starting row index for pagination.  [default: 0]
* `-n, --num-rows INTEGER`: Number of rows to retrieve.  [default: 100]
* `--json`: Output in JSON format.

## `datascribe_cli data-tables-for-user`

Retrieve and display all data tables that the authenticated user has access to.

**Usage**:

```console
$ datascribe_cli data-tables-for-user [OPTIONS]
```

**Options**:

* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--json`: Output in JSON format.

---

## `datascribe_cli data-table-rows`

Retrieve and display rows from a specified data table, allowing you to specify which columns to include. Filtering is supported using --filter.

**Usage**:

```console
$ datascribe_cli data-table-rows [OPTIONS]
```

**Options**:

* `-t, --table-name TEXT`: Name of the data table.  [required]
* `-c, --columns TEXT`: Comma-separated list of columns.  [required]
* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `-s, --starting-row INTEGER`: Starting row index for pagination.  [default: 0]
* `-n, --num-rows INTEGER`: Number of rows to retrieve.  [default: 100]
* `--filter TEXT`: Filter expression. Can be used multiple times.
* `--json`: Output in JSON format.

---

## `datascribe_cli data-table-columns`

Retrieve and display the columns of a specified data table.

**Usage**:

```console
$ datascribe_cli data-table-columns [OPTIONS]
```

**Options**:
*
* `-t, --table-name TEXT`: Name of the data table.  [required]
* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--json`: Output in JSON format.

---

## `datascribe_cli data-table-metadata`

Retrieve and display metadata for a specified data table.

**Usage**:

```console
$ datascribe_cli data-table-metadata [OPTIONS]
```

**Options**:

* `-t, --table-name TEXT`: Name of the data table.  [required]
* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--json`: Output in JSON format.

---

## `datascribe_cli data-table-rows-count`

Retrieve and display the number of rows in a specified data table. Filtering is supported using --filter.

**Usage**:

```console
$ datascribe_cli data-table-rows-count [OPTIONS]
```

**Options**:

* `-t, --table-name TEXT`: Name of the data table.  [required]
* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--filter TEXT`: Filter expression. Can be used multiple times.
* `--json`: Output in JSON format.

---

## `datascribe_cli get-material-by-id`

Get material details by ID from selected providers.

**Usage**:

```console
$ datascribe_cli get-material-by-id [OPTIONS]
```

**Options**:

* `-i, --ids TEXT`: Material IDs to retrieve (e.g., mp-190, aflow:xxxx).  [required]
* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--mp`: Query Materials Project provider.
* `--aflow`: Query AFLOW provider.
* `--json`: Output in JSON format.

---

## `datascribe_cli search-materials`

Search for materials using formula, elements, and other filters.

**Usage**:

```console
$ datascribe_cli search-materials [OPTIONS]
```

**Options**:

* `-f, --formula TEXT`: Chemical formula to search for (e.g., SiO2, Fe2O3).  [required]
* `-e, --elements TEXT`: Comma-separated list of required elements (e.g., Si,O).  [required]
* `-x, --exclude-elements TEXT`: Comma-separated list of elements to exclude (e.g., Pb,Hg).  [required]
* `-g, --spacegroup TEXT`: Space group or crystal system to filter by (e.g., cubic, Pnma).  [required]
* `-p, --props TEXT`: Comma-separated list of properties to include (e.g., band_gap,formation_energy).  [required]
* `-t, --temperature TEXT`: Temperature filter (if supported by provider).  [required]
* `--api-key TEXT`: Your DataScribe API key.  [env var: DATASCRIBE_API_TOKEN; required]
* `--mp`: Query Materials Project provider.
* `--aflow`: Query AFLOW provider.
* `--oqmd`: Query OQMD provider.
* `--page INTEGER`: Page number for paginated results.   [default: 1]
* `--size INTEGER`: Number of results per page.   [default: 50]
* `--json`: Output in JSON format.
