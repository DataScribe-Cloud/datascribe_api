# Models

The DataScribe API uses Pydantic models to provide type-safe data structures for all API responses. All models include:

- **Full type validation**: Automatic validation of data types and structure
- **IDE support**: Auto-completion and type hints in your editor
- **Serialization**: Easy conversion to JSON, dicts, and DataFrames
- **Documentation**: Built-in field descriptions and examples

## Available Models

### Data Table Models

- **[DataTable](DataTable.md)**: Represents a single data table with metadata
- **[DataTables](DataTables.md)**: Collection of data tables
- **[DataTableRows](DataTableRows.md)**: Collection of rows from a table query
- **[DataTableColumns](DataTableColumns.md)**: Column definitions for a table
- **[DataTableMetadata](DataTableMetadata.md)**: Complete metadata for a table
- **[DataTableRowsCount](DataTableRowsCount.md)**: Row count information

### Materials Models

- **[MaterialSearchResults](MaterialSearchResults.md)**: Results from a materials search
- **[MaterialByIdResults](MaterialByIdResults.md)**: Results from a material ID lookup

## Common Methods

All collection models (DataTables, DataTableRows, DataTableColumns, MaterialSearchResults, MaterialByIdResults) support these methods:

### to_dataframe()

```python title="Convert the model data to a pandas DataFrame"
from datascribe_api import DataScribeClient

client = DataScribeClient()
tables = client.get_data_tables_for_user()

# Convert to DataFrame
df = tables.to_dataframe()
print(df.head())
```

### to_list()

```python title="Convert the model data to a list of dictionaries"
rows = client.get_data_table(tableName="my_table")

# Convert to list
data = rows.to_list()
for row_dict in data:
    print(row_dict)
```

## Model Serialization

All models support standard Pydantic serialization:

```python title="To dictionary"
data_dict = model.model_dump()
```

```python title="To JSON string"
json_str = model.model_dump_json()
```

```python title="To JSON with indentation"
json_pretty = model.model_dump_json(indent=2)
```

```python title="Exclude certain fields"
data_dict = model.model_dump(exclude={"user_id"})
```

```python title="Include only certain fields"
data_dict = model.model_dump(include={"table_name", "display_name"})
```
