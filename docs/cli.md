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
datascribe_cli data-tables-for-user --api-key "your_api_key"
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
datascribe_cli data-tables [OPTIONS]
```

**Options:**

`--api-key TEXT`
    :   Your DataScribe API key

`--json`
    :   Output in JSON format

```bash title="Examples"
# Pretty-printed output
datascribe_cli data-tables

# JSON output
datascribe_cli data-tables --json

# With explicit API key
datascribe_cli data-tables --api-key "your_key"
```

---

### `data-tables-for-user`

List all data tables owned by your user account.

```bash title="Usage"
datascribe_cli data-tables-for-user [OPTIONS]
```

**Options:**

`--api-key TEXT`
    :   Your DataScribe API key

`--json`
    :   Output in JSON format

```bash title="Examples"
# List your tables
datascribe_cli data-tables-for-user

# JSON output
datascribe_cli data-tables-for-user --json > my_tables.json
```

---

### `data-table`

Retrieve rows from a specific data table.

```bash title="Usage"
datascribe_cli data-table [OPTIONS]
```

**Options:**

`--table-name, -t TEXT`
    :   Name of the data table  [required]

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
datascribe_cli data-table --table-name my_experiments

# Get specific range
datascribe_cli data-table --table-name my_experiments --starting-row 1000 --num-rows 500

# Using short flags
datascribe_cli data-table -t my_experiments -s 0 -n 50

# JSON output
datascribe_cli data-table -t my_experiments --json
```

---

### `data-table-rows`

Query table rows with advanced filtering and column selection.

```bash title="Usage"
datascribe_cli data-table-rows [OPTIONS]
```

**Options:**

`--table-name, -t TEXT`
    :   Name of the data table  [required]

`--columns, -c TEXT`
    :   Comma-separated list of columns  [required]

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
datascribe_cli data-table-rows --table-name experiments \
  --filter "temperature > 300"

# Multiple filters (AND logic)
datascribe_cli data-table-rows --table-name experiments \
  --filter "temperature > 300" \
  --filter "pressure < 100" \
  --filter "element in Fe,Ni,Co"

# Pattern matching
datascribe_cli data-table-rows --table-name materials \
  --filter "formula like %O3"

# Null checks
datascribe_cli data-table-rows --table-name results \
  --filter "error is null"

# Complex query with pagination
datascribe_cli data-table-rows --table-name large_dataset \
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
datascribe_cli data-table-columns [OPTIONS]
```

**Options:**

`--table-name, -t TEXT`
    :   Name of the data table  [required]

`--api-key TEXT`
    :   Your DataScribe API key

`--json`
    :   Output in JSON format

```bash title="Examples"
# Show columns
datascribe_cli data-table-columns --table-name my_table

# JSON output
datascribe_cli data-table-columns -t my_table --json
```

---

### `data-table-metadata`

Get complete metadata for a data table, including schema and timestamps.

```bash title="Usage"
datascribe_cli data-table-metadata [OPTIONS]
```

**Options:**

`--table-name, -t TEXT`
    :   Name of the data table  [required]

`--api-key TEXT`
    :   Your DataScribe API key

`--json`
    :   Output in JSON format

```bash title="Examples"
# Show metadata
datascribe_cli data-table-metadata --table-name my_table

# JSON output
datascribe_cli data-table-metadata -t my_table --json
```

---

### `data-table-rows-count`

Get the total number of rows in a data table, optionally with filters.

```bash title="Usage"
datascribe_cli data-table-rows-count [OPTIONS]
```

**Options:**

`--table-name, -t TEXT`
    :   Name of the data table  [required]

`--api-key TEXT`
    :   Your DataScribe API key

`--filter, -f TEXT`
    :   Filter expression (can be used multiple times)

`--json`
    :   Output in JSON format

```bash title="Examples"
# Total row count
datascribe_cli data-table-rows-count --table-name my_table

# Count with filters
datascribe_cli data-table-rows-count -t experiments \
  --filter "temperature > 300" \
  --filter "status == completed"

# JSON output
datascribe_cli data-table-rows-count -t my_table --json
```

---

### `search-materials`

Search for materials across multiple data providers.

```bash title="Usage"
datascribe_cli search-materials [OPTIONS]
```

**Options:**

`--formula, -f TEXT`
    :   Chemical formula to search for (e.g., SiO2, Fe2O3)

`--elements, -e TEXT`
    :   Comma-separated list of required elements (e.g., Si,O)

`--exclude-elements, -x TEXT`
    :   Comma-separated list of elements to exclude (e.g., Pb,Hg)

`--spacegroup, -g TEXT`
    :   Space group or crystal system to filter by (e.g., cubic, Pnma)

`--props, -p TEXT`
    :   Comma-separated list of properties to include (e.g., band_gap,formation_energy)

`--temperature, -t TEXT`
    :   Temperature filter (if supported by provider)

`--mp`
    :   Query Materials Project provider

`--aflow`
    :   Query AFLOW provider

`--oqmd`
    :   Query OQMD provider

`--page INTEGER`
    :   Page number for paginated results   [default: 1]

`--size INTEGER`
    :   Number of results per page   [default: 50]

`--api-key TEXT`
    :   Your DataScribe API key

`--json`
    :   Output in JSON format

```bash title="Examples"
# Search by formula
datascribe_cli search-materials --formula "Fe2O3"

# Search by elements
datascribe_cli search-materials --elements Fe,O

# Search with specific providers
datascribe_cli search-materials \
  --formula "TiO2" \
  --mp --aflow

# Limit results
datascribe_cli search-materials \
  --elements Fe,Ni \
  --size 50

# JSON output
datascribe_cli search-materials \
  --formula "Fe2O3" \
  --json > iron_oxide_materials.json
```

---

### `get-material-by-id`

Retrieve specific materials by their unique identifiers.

```bash title="Usage"
datascribe_cli get-material-by-id [OPTIONS]
```

**Options:**

`-i, --ids TEXT`
    :   Material IDs to retrieve (e.g., mp-190, aflow:xxxx)  [required]

`--api-key TEXT`
    :   Your DataScribe API key  [env var: DATASCRIBE_API_TOKEN; required]

`--mp`
    :   Query Materials Project provider

`--aflow`
    :   Query AFLOW provider

`--api-key TEXT`
    :   Your DataScribe API key

`--json`
    :   Output in JSON format

```bash title="Examples"
# Single material
datascribe_cli get-material-by-id --ids mp-149

# Multiple materials
datascribe_cli get-material-by-id --ids mp-149,mp-13,mp-22526

# Specific providers
datascribe_cli get-material-by-id -i mp-149 \
  --mp

# JSON output
datascribe_cli get-material-by-id -i mp-149,mp-13 \
  --mp \
  --json
```

---

## Getting Help

Every command supports `--help`:

```bash
# General help
datascribe_cli --help

# Command-specific help
datascribe_cli data-table-rows --help
datascribe_cli search-materials --help
```
