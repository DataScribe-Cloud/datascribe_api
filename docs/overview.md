# Overview

The DataScribe API provides programmatic access to the DataScribe Cloud platform, a comprehensive solution for managing and querying scientific data tables and materials science databases.

## What Can You Do?

### Data Table Operations

- **List Tables**: View all available data tables or just your own
- **Query Tables**: Retrieve rows with pagination and filtering
- **Inspect Metadata**: Access table schemas, column types, and creation timestamps
- **Count Rows**: Get the total number of rows in a table
- **View Columns**: List all columns with their data types and properties

### Materials Science Data

- **Search Materials**: Query materials by formula, elements, or properties
- **Get by ID**: Retrieve specific materials by their unique identifiers
- **Multiple Providers**: Access data from Materials Project, AFLOW, and other sources
- **Rich Metadata**: Get provenance, properties, and crystal systems

### Advanced Features

- **Filtering**: Build complex queries with operators like `==`, `>`, `<`, `in`, `like`, and more
- **Pagination**: Efficiently retrieve large datasets in manageable chunks
- **Data Export**: Convert results to pandas DataFrames or Python lists
- **Type Safety**: Full Pydantic model validation for reliable data handling

## Authentication

All API requests require authentication using an API key. You can provide it in two ways:

1. **Environment Variable** (recommended):
   ```bash
   export DATASCRIBE_API_TOKEN="your_api_key"
   ```

2. **Direct Parameter**:
   ```python
   with DataScribeClient(api_key="your_api_key") as client:
       tables = client.get_data_tables_for_user()
   ```
