---
title: "Quick Start: Python API"
---

This guide shows how to use the DataScribe Python API for accessing tables, rows, columns, metadata, and materials. All objects support conversion to pandas DataFrames and Python lists for easy analysis.

## Basic Usage

Retrieve all tables available to the user and convert them to a DataFrame or Python list for further analysis.

```python
from datascribe_api import DataScribeClient

with DataScribeClient() as client:  # (1)!
    tables = client.get_data_tables_for_user()
    for table in tables:
        print(f"Table: {table.table_name}")
        print(f"  Display Name: {table.display_name}")
        print(f"  Created: {table.created_on}")
```

1. Uses `DATASCRIBE_API_TOKEN` environment variable for authentication.

## Query a Data Table

Fetch rows from a specific data table and convert them for analysis.

```python
from datascribe_api import DataScribeClient

with DataScribeClient(api_key="your_api_key") as client:
    rows = client.get_data_table(
        tableName="my_table",
        numRows=100
    )
    for row in rows:
        print(row)
    # Convert rows to DataFrame or list
    df = rows.to_dataframe()
    lst = rows.to_list()
```

## Filter Rows

Apply simple or complex filters to retrieve rows matching specific conditions.

```python
from datascribe_api import DataScribeClient
from datascribe_api.filter import Filter

with DataScribeClient(api_key="your_api_key") as client:
    filter_query = Filter("temperature") > 300
    rows = client.get_data_table_rows(
        tableName="experiments",
        filters=filter_query,
        numRows=50
    )

    # Complex filters
    complex_filter = (
        (Filter("element").in_(["Fe", "Ni", "Co"])) &
        (Filter("formation_energy") < -0.5) &
        (Filter("bandgap").is_not_null())
    )
    rows = client.get_data_table_rows(
        tableName="materials",
        filters=complex_filter
    )
```

## Get Table Columns

Retrieve column names and types for a table, and convert them for schema inspection or selection.

```python
from datascribe_api import DataScribeClient

with DataScribeClient(api_key="your_api_key") as client:
    columns = client.get_data_table_columns(tableName="my_table")
    for col in columns.columns:
        print(f"{col.column_name}: {col.data_type}")
```

## Get Table Metadata

Get metadata such as type, visibility, and timestamps for a table.

```python
from datascribe_api import DataScribeClient

with DataScribeClient(api_key="your_api_key") as client:
    metadata = client.get_data_table_metadata(tableName="my_table")
    print(f"Table Type: {metadata.table_type}")
    print(f"Visibility: {metadata.visibility}")
    print(f"Last Updated: {metadata.last_updated}")
```

## Get Row Count

Get the number of rows in a table for pagination or summary statistics.

```python
from datascribe_api import DataScribeClient

with DataScribeClient(api_key="your_api_key") as client:
    count = client.get_data_table_rows_count(tableName="my_table")
    print(f"Total Rows: {count.total_rows}")
```

## Search Materials

Search for materials by formula, elements, and provider for further analysis.

```python
from datascribe_api import DataScribeClient

with DataScribeClient(api_key="your_api_key") as client:
    results = client.search_materials(
        formula="Fe2O3",
        elements=["Fe", "O"],
        providers=["MP", "AFLOW"]
    )
    print(f"Found {results.total} materials")
    for material in results.results:
        print(f"ID: {material.material_id}")
        print(f"Formula: {material.formula}")
        print(f"Elements: {material.elements}")
        print(f"Properties: {material.key_props}")
```

## Get Material by ID

Get material details by ID from selected providers.

```python
from datascribe_api import DataScribeClient

with DataScribeClient(api_key="your_api_key") as client:
    results = client.get_material_by_id(
        ids=["mp-149", "mp-13"],
        providers=["MP"]
    )
    for result in results.results:
        print(f"Provider: {result.provider}")
        print(f"ID: {result.id}")
        print(f"Data: {result.data}")
```
