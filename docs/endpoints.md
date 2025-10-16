---
title: "API Endpoints"
hide:
  - navigation
  - toc
---

# DataScribe API Endpoints

This page lists all available endpoints in the DataScribe API, including their HTTP paths, parameters, and descriptions.

| Endpoint Name             | HTTP Path                   | Parameters                                                                                 | Description                               |
|---------------------------|-----------------------------|--------------------------------------------------------------------------------------------|-------------------------------------------|
| `get_data_tables`           | /data/data-tables           | –                                                                                          | List all data tables (admin only)         |
| `get_data_tables_for_user`  | /data/data-tables-for-user  | –                                                                                          | List data tables available to the user    |
| `get_data_table`            | /data/data-table            | tableName, startingRow, numRows                                                            | Get rows from a data table                |
| `get_data_table_rows`       | /data/data-table-rows       | tableName, columns, startingRow, numRows, filters                                          | Get rows from a data table (with columns) |
| `get_data_table_rows_count` | /data/data-table-rows-count | tableName, filters                                                                         | Get row count for a data table            |
| `get_data_table_columns`    | /data/data-table-columns    | tableName                                                                                  | Get columns of a data table               |
| `get_data_table_metadata`   | /data/data-table-metadata   | tableName                                                                                  | Get metadata for a data table             |
| `get_material_by_id`        | /materials                  | ids, providers                                                                             | Get material by IDs                       |
| `search_materials`          | /materials/search           | formula, elements, exclude_elements, spacegroup, props, <br/>temperature, providers, page, size | Search for materials                      |
