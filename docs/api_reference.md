# Python API Reference

Complete reference for the DataScribe Python client.

## Client Methods

### Data Table Methods

#### get_data_tables()

Get all data tables in the system (requires admin privileges).

**Returns:** `DataTables` - Collection of all data tables

```python title="Example"
client = DataScribeClient(api_key="admin_key")
tables = client.get_data_tables()
for table in tables:
    print(table.table_name)
```

---

#### get_data_tables_for_user()

Get all data tables owned by the authenticated user.

**Returns:** `DataTables` - Collection of user's data tables

```python title="Example"
tables = client.get_data_tables_for_user()
print(f"You have {len(tables)} tables")
```

---

#### get_data_table()

Query rows from a specific data table.

**Parameters:**

`tableName` (str) - Name of the table to query

`startingRow` (int, _optional_) - Starting row index for pagination (default: 0)

`numRows` (int, _optional_) - Number of rows to retrieve (default: 100)

**Returns:** `DataTableRows` - Collection of table rows

```python title="Example"
rows = client.get_data_table(
    tableName="my_experiments",
    startingRow=0,
    numRows=50
)

# Iterate over rows
for row in rows:
    print(row._datascribe_user, row.temperature)
```

---

#### get_data_table_rows()

Query table rows with advanced filtering and column selection.

**Parameters:**

`tableName` (str) - Name of the table to query

`columns` (list, _optional_) - List of columns to retrieve

`filters` (Filter, _optional_) - Filter expression to apply

`startingRow` (int, _optional_) - Starting row index (default: 0)

`numRows` (int, _optional_) - Number of rows to retrieve (default: 100)

**Returns:** `DataTableRows` - Filtered collection of table rows

```python title="Example"
from datascribe_api.filter import Filter

# Simple filter
rows = client.get_data_table_rows(
    tableName="experiments",
    filters=Filter("temperature") > 300,
    numRows=100
)

# Complex filter with column selection
columns = client.get_data_table_columns(tableName="experiments")
filter_query = (
    (Filter("temperature") > 300) &
    (Filter("status") == "completed")
)

rows = client.get_data_table_rows(
    tableName="experiments",
    columns=columns.to_list(),
    filters=filter_query
)
```

---

#### get_data_table_columns()

Get column definitions for a data table.

**Parameters:** `tableName` (str) - Name of the table

**Returns:** `DataTableColumns` - Column definitions and metadata

```python title="Example"
columns = client.get_data_table_columns(tableName="my_table")

# Access columns
for col in columns.columns:
    print(f"{col.column_name}: {col.data_type}")
```

---

#### get_data_table_metadata()

Get complete metadata for a data table.

**Parameters:** `tableName` (str): Name of the table

**Returns:** `DataTableMetadata` - Complete table metadata

```python title="Example"
metadata = client.get_data_table_metadata(tableName="my_table")

print(f"Display Name: {metadata.display_name}")
print(f"Created: {metadata.created_on}")
print(f"Last Updated: {metadata.last_updated}")
print(f"Type: {metadata.table_type}")
print(f"Visibility: {metadata.visibility}")

# Access schema
for col in metadata.database_schema.columns:
    print(f"{col.column_name}: {col.column_type}")
```

---

#### get_data_table_rows_count()

Get the total number of rows in a data table.

**Parameters:**

`tableName` (str) - Name of the table

`filters` (Filter, _optional_) - Filter expression to apply

**Returns:** `DataTableRowsCount` - Row count information

```python title="Example"
# Total count
count = client.get_data_table_rows_count(tableName="my_table")
print(f"Total rows: {count.total_rows}")

# Filtered count
from datascribe_api.filter import Filter
count = client.get_data_table_rows_count(
    tableName="experiments",
    filters=Filter("status") == "completed"
)
print(f"Completed experiments: {count.total_rows}")
```

---

### Materials Methods

#### search_materials()

Search for materials across multiple data providers.

**Parameters:**

`formula` (str, _optional_) - Chemical formula to search for

`elements` (list or str, _optional_) - Elements to include in the search

`exclude_elements` (list or str, _optional_) - Elements to exclude from the search results

`spacegroup` (str, _optional_) - Space group symbol or number to filter materials

`props` (list or str, _optional_) - Material properties to filter or retrieve

`temperature` (str, _optional_) - Temperature condition for property-based queries

`providers` (list or str, _optional_) - Data providers to search (e.g., "MP", "AFLOW")

`page` (int, _optional_) - Page number for paginated results (default: 1)

`size` (int, _optional_) - Number of results per page (default: 50)


**Returns:** `MaterialSearchResults` - Search results with material summaries

```python title="Example"
# Search by formula
results = client.search_materials(formula="Fe2O3")

# Search by elements
results = client.search_materials(elements=["Fe", "O"])

# Search with specific providers
results = client.search_materials(
    formula="TiO2",
    providers=["MP", "AFLOW"],
)

# Access results
print(f"Found {results.total} materials")
for material in results.results:
    print(f"ID: {material.material_id}")
    print(f"Formula: {material.formula}")
    print(f"Elements: {material.elements}")
    print(f"Properties: {material.key_props}")
```

---

#### get_material_by_id()

Retrieve specific materials by their unique identifiers.

**Parameters:**

`ids` (list or str) - Material ID(s) to retrieve

`providers` (list or str, _optional_) - Data providers to query

**Returns:** `MaterialByIdResults` - Material data from providers

```python title="Example"
# Single material
results = client.get_material_by_id(ids="mp-149")

# Multiple materials
results = client.get_material_by_id(
    ids=["mp-149", "mp-13", "mp-22526"],
    providers=["MP"]
)

# Access results
for result in results.results:
    print(f"Provider: {result.provider}")
    print(f"ID: {result.id}")
    print(f"Data: {result.data}")
```

---

## Filter Class

The `Filter` class enables building complex query expressions.

### Creating Filters

```python
from datascribe_api.filter import Filter

# Simple comparison
f1 = Filter("temperature") > 300
f2 = Filter("status") == "completed"
f3 = Filter("element") != "Fe"
```

### Filter Operators

#### Comparison Operators

```python
Filter("value") > 10      # Greater than
Filter("value") >= 10     # Greater than or equal
Filter("value") < 10      # Less than
Filter("value") <= 10     # Less than or equal
Filter("value") == 10     # Equal to
Filter("value") != 10     # Not equal to
```

#### Membership Operators

```python
Filter("element").in_(["Fe", "Ni", "Co"])         # IN
Filter("element").not_in(["He", "Ne", "Ar"])      # NOT IN
```

#### String Matching

```python
Filter("formula").like("%O3")       # SQL LIKE (case-sensitive)
Filter("formula").ilike("%o3")      # SQL ILIKE (case-insensitive)
```

#### Null Checks

```python
Filter("error").is_null()           # IS NULL
Filter("result").is_not_null()      # IS NOT NULL
```

### Combining Filters

```python
# AND (&)
combined = (Filter("temperature") > 300) & (Filter("pressure") < 100)

# OR (|)
combined = (Filter("element") == "Fe") | (Filter("element") == "Ni")

# Complex combinations
complex_filter = (
    (Filter("temperature") > 300) &
    (Filter("element").in_(["Fe", "Ni", "Co"])) &
    (Filter("bandgap").is_not_null())
)
```

### Using Filters

```python title="with get_data_table_rows"
rows = client.get_data_table_rows(
    tableName="experiments",
    filters=Filter("temperature") > 300
)
```

```python title="with get_data_table_rows_count"
count = client.get_data_table_rows_count(
    tableName="experiments",
    filters=(
        (Filter("status") == "completed") &
        (Filter("year") >= 2020)
    )
)
```
