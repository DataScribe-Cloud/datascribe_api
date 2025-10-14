# Installation & Quick Start

## Installation

Install the DataScribe API using pip:

```bash
pip install datascribe-api
```

For development:

```bash
git clone https://github.com/DataScribe-Cloud/datascribe_api.git
cd datascribe_api
pip install -e .
```

## Requirements

- Python 3.11 or higher
- An active DataScribe account and API key

## Get Your API Key

1. Visit [https://datascribe.cloud/profile](https://datascribe.cloud/profile)
2. Log in or create an account
3. Navigate to the API Keys section
4. Generate a new API key
5. Copy and save it securely

## Configuration

Set your API key as an environment variable:

### Linux/macOS

```bash
export DATASCRIBE_API_TOKEN="your_api_key_here"
```

Add to `~/.bashrc` or `~/.zshrc` for persistence:

```bash
echo 'export DATASCRIBE_API_TOKEN="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### Windows (PowerShell)

```powershell
$env:DATASCRIBE_API_TOKEN="your_api_key_here"
```

For persistence:

```powershell
[System.Environment]::SetEnvironmentVariable('DATASCRIBE_API_TOKEN', 'your_api_key_here', 'User')
```
