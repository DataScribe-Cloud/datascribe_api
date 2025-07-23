<div align="center">

# DataScribe API Client

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://opensource.org/license/gpl-3-0)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Platforms](https://img.shields.io/badge/platform-linux%20%7C%20macos%20%7C%20windows-lightgrey)

`datascribe_api` is a Python client for interacting with the DataScribe API. It allows users to search for data tables and their metadata, automating data retrieval and analysis workflows.

<p>
  <a href="https://github.com/DataScribe-Cloud/datascribe_api/issues/new?labels=bug">Report a Bug</a> |
  <a href="https://github.com/DataScribe-Cloud/datascribe_api/issues/new?labels=enhancement">Request a Feature</a>
</p>

</div>

---

## Features

- Search and retrieve data tables and metadata from the DataScribe API
- Simple Python interface for querying endpoints
- Automatic model mapping for API responses
- Context manager support for resource management

---

## Installation

You can use pip to install the `datascribe_api` package directly from PyPI:

```sh
pip install datascribe_api
```

---

## Quick Start

### Python Client Usage
To get started with the `datascribe_api`, you can use the following example to retrieve and print the names of data tables available to the user:
```python
from datascribe_api import DataScribeClient

with DataScribeClient(api_key="YOUR_API_TOKEN") as client:
    tables = client.get_data_tables_for_user()
    for table in tables:
        print(f"Table Name: {table.display_name}")
```

Make sure to replace the `DataScribeClient` initialization with your actual API key or store it in an environment variable named `DATASCRIBE_API_TOKEN` for authentication.

### CLI Usage

You can also use the command-line interface to interact with the DataScribe API. Here are some examples:
```sh
# List all data tables for the authenticated user
datascribe_api data-tables-for-user
```

See the [CLI documentation](./src/datascribe_cli/README_CLI.md) for more commands and options.

---

## License

This project is licensed under the GNU GPLv3 License. See the [LICENSE](./LICENSE) file for details.

---
