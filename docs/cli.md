# CLI Usage

The DataScribe CLI provides a command-line interface for interacting with the DataScribe API. All commands support the `--help` flag for detailed information.

## Installation

The CLI is installed automatically with the DataScribe API:

```bash
pip install datascribe-api
```

## Configuration

Set your API key as an environment variable:

```bash
export DATASCRIBE_API_TOKEN="your_api_key"
```

Alternatively, pass it with every command using `--api-key` (**not recommended!**):

```bash
datascribe-api data-tables-for-user --api-key "your_api_key"
```

## Global Options

Most commands support these options:

- `--api-key`: Your DataScribe API key (or set `DATASCRIBE_API_TOKEN`)
- `--json`: Output in JSON format instead of pretty-printed
- `--help`: Show help information

## Commands

### `data-tables`

List all available data tables (requires admin privileges).

```bash title="Usage"
datascribe-api data-tables [OPTIONS]
```

**Options:**

`--api-key TEXT`
    :   Your DataScribe API key

`--json`
    :   Output in JSON format

```bash title="Examples"
# Pretty-printed output
datascribe-api data-tables

# JSON output
datascribe-api data-tables --json

# With explicit API key
datascribe-api data-tables --api-key "your_key"
```

---

### `data-tables-for-user`

List all data tables owned by your user account.

```bash title="Usage"
datascribe-api data-tables-for-user [OPTIONS]
```

**Options:**

`--api-key TEXT`
    :   Your DataScribe API key

`--json`
    :   Output in JSON format

```bash title="Examples"
# List your tables
datascribe-api data-tables-for-user

# JSON output
datascribe-api data-tables-for-user --json > my_tables.json
```

---

### `data-table`

Retrieve rows from a specific data table.

```bash title="Usage"
datascribe-api data-table TABLE_NAME [OPTIONS]
```

**Arguments:**

`TABLE_NAME`
    :   Name of the data table (required)

**Options:**

`--api-key TEXT`
    :   Your DataScribe API key

`--starting-row, -s INTEGER`
    :   Starting row index (default: 0)

`--num-rows, -n INTEGER`
    :   Number of rows to retrieve (default: 100)

`--json`
    :   Output in JSON format

```bash title="Examples"
# Get first 100 rows
datascribe-api data-table my_experiments

# Get specific range
datascribe-api data-table my_experiments --starting-row 1000 --num-rows 500

# Using short flags
datascribe-api data-table my_experiments -s 0 -n 50

# JSON output
datascribe-api data-table my_experiments --json
```

---

### `data-table-rows`

Query table rows with advanced filtering and column selection.

```bash title="Usage"
datascribe-api data-table-rows TABLE_NAME [OPTIONS]
```

**Arguments:**

`TABLE_NAME`
    :   Name of the data table (required)

**Options:**

`--api-key TEXT`
    :   Your DataScribe API key

`--starting-row, -s INTEGER`
    :   Starting row index (default: 0)

`--num-rows, -n INTEGER`
    :   Number of rows to retrieve (default: 100)

`--filter, -f TEXT`
    :   Filter expression (can be used multiple times)

`--json`
    :   Output in JSON format

**Filter Syntax:**

- Comparison: `column > value`, `column == value`, `column != value`
- Range: `column >= value`, `column <= value`
- Membership: `column in value1,value2`, `column not in value1,value2`
- Pattern: `column like %pattern%`, `column ilike %pattern%` (case-insensitive)
- Null checks: `column is null`, `column is not null`

```bash title="Examples"
# Single filter
datascribe-api data-table-rows experiments \
  --filter "temperature > 300"

# Multiple filters (AND logic)
datascribe-api data-table-rows experiments \
  --filter "temperature > 300" \
  --filter "pressure < 100" \
  --filter "element in Fe,Ni,Co"

# Pattern matching
datascribe-api data-table-rows materials \
  --filter "formula like %O3"

# Null checks
datascribe-api data-table-rows results \
  --filter "error is null"

# Complex query with pagination
datascribe-api data-table-rows large_dataset \
  --filter "year >= 2020" \
  --filter "status == completed" \
  --starting-row 1000 \
  --num-rows 100 \
  --json
```

---

### `data-table-columns`

Get column definitions and metadata for a data table.

```bash title="Usage"
datascribe-api data-table-columns TABLE_NAME [OPTIONS]
```

**Arguments:**

`TABLE_NAME`
    :   Name of the data table (required)

**Options:**

`--api-key TEXT`
    :   Your DataScribe API key

`--json`
    :   Output in JSON format

```bash title="Examples"
# Show columns
datascribe-api data-table-columns my_table

# JSON output
datascribe-api data-table-columns my_table --json
```

---

### `data-table-metadata`

Get complete metadata for a data table, including schema and timestamps.

```bash title="Usage"
datascribe-api data-table-metadata TABLE_NAME [OPTIONS]
```

**Arguments:**

`TABLE_NAME`
    :   Name of the data table (required)

**Options:**

`--api-key TEXT`
    :   Your DataScribe API key

`--json`
    :   Output in JSON format

```bash title="Examples"
# Show metadata
datascribe-api data-table-metadata my_table

# JSON output
datascribe-api data-table-metadata my_table --json
```

---

### `data-table-rows-count`

Get the total number of rows in a data table, optionally with filters.

```bash title="Usage"
datascribe-api data-table-rows-count TABLE_NAME [OPTIONS]
```

**Arguments:**

`TABLE_NAME`
    :   Name of the data table (required)

**Options:**

`--api-key TEXT`
    :   Your DataScribe API key

`--filter, -f TEXT`
    :   Filter expression (can be used multiple times)

`--json`
    :   Output in JSON format

```bash title="Examples"
# Total row count
datascribe-api data-table-rows-count my_table

# Count with filters
datascribe-api data-table-rows-count experiments \
  --filter "temperature > 300" \
  --filter "status == completed"

# JSON output
datascribe-api data-table-rows-count my_table --json
```

---

### `search-materials`

Search for materials across multiple data providers.

```bash title="Usage"
datascribe-api search-materials [OPTIONS]
```

**Options:**

`--api-key TEXT`
    :   Your DataScribe API key

`--formula TEXT`
    :   Chemical formula to search for

`--elements TEXT`
    :   Comma-separated list of elements

`--providers TEXT`
    :   Comma-separated list of providers (e.g., materials_project,aflow)

`--limit INTEGER`
    :   Maximum number of results (default: 100)

`--json`
    :   Output in JSON format

```bash title="Examples"
# Search by formula
datascribe-api search-materials --formula "Fe2O3"

# Search by elements
datascribe-api search-materials --elements Fe,O

# Search with specific providers
datascribe-api search-materials \
  --formula "TiO2" \
  --providers materials_project,aflow

# Limit results
datascribe-api search-materials \
  --elements Fe,Ni \
  --limit 50

# JSON output
datascribe-api search-materials \
  --formula "Fe2O3" \
  --json > iron_oxide_materials.json
```

---

### `get-material-by-id`

Retrieve specific materials by their unique identifiers.

```bash title="Usage"
datascribe-api get-material-by-id IDS [OPTIONS]
```

**Arguments:**

`IDS`
    :   Comma-separated list of material IDs (required)

**Options:**

`--api-key TEXT`
    :   Your DataScribe API key

`--providers TEXT`
    :   Comma-separated list of providers

`--json`
    :   Output in JSON format

```bash title="Examples"
# Single material
datascribe-api get-material-by-id mp-149

# Multiple materials
datascribe-api get-material-by-id mp-149,mp-13,mp-22526

# Specific providers
datascribe-api get-material-by-id mp-149 \
  --providers materials_project

# JSON output
datascribe-api get-material-by-id mp-149,mp-13 \
  --providers materials_project \
  --json
```

---

## Getting Help

Every command supports `--help`:

```bash
# General help
datascribe-api --help

# Command-specific help
datascribe-api data-table-rows --help
datascribe-api search-materials --help
```
