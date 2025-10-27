---
title: "Quick Start: Command-Line Interface"
---

Interact with the DataScribe API from your terminal. The CLI provides commands to list tables, query data, filter rows, inspect metadata, and search materials.

## Usage

```console
$ datascribe_cli [OPTIONS] COMMAND [ARGS]...
```

### Global Options

- `--install-completion`: Install shell completion.
- `--show-completion`: Show shell completion script.

## Basic Commands

List and query tables, inspect columns, metadata, and row counts:

```bash title="List tables available to the authenticated user"
$ datascribe_cli data-tables-for-user --api-key YOUR_API_KEY
```

```bash title="List all tables (admin only)"
$ datascribe_cli data-tables
```

```bash title="Query a table"
$ datascribe_cli data-table -t my_table --num-rows 100
```

```bash title="Get table columns"
$ datascribe_cli data-table-columns -t my_table
```

```bash title="Get table metadata"
$ datascribe_cli data-table-metadata -t my_table
```

```bash title="Get row count"
$ datascribe_cli data-table-rows-count -t my_table
```

## Filtering Rows

Filter rows using expressions and output as JSON:

```bash
$ datascribe_cli data-table-rows \
    -t my_table \
    -c col1,col2 \
    --filter "temperature > 300" \
    --filter "element in Fe,Ni,Co" \
    --num-rows 50 \
    --json > output.json
```

## Materials Search

Search for materials:

```bash
$ datascribe_cli search-materials \
    --formula "Fe2O3" \
    --elements Fe,O \
    --mp \
    --aflow
```

Get materials by ID
```bash
$ datascribe_cli get-material-by-id \
    --ids mp-149,mp-13 \
    --mp
```

## Help

For more details on each command, use:

```bash
$ datascribe_cli COMMAND --help
```
