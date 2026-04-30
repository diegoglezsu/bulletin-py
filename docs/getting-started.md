# Getting Started

## Requirements 🐍

- Python 3.7+
- Internet access for live EUR-Lex queries

## Installation

Install from PyPI:

```bash
pip install bulletin-fetcher
```

Install development dependencies (project clone):

```bash
pip install -e .[dev]
```

## First Query 🚀

```python
from bulletin.eurlex.api.client import EurlexBulletinClient

client = EurlexBulletinClient()
acts = client.get_acts( 
    date="2025-01-01",
    date_end="2025-03-31",
    title_contains="artificial intelligence",
    language="ENG"
)

print(f"Total acts: {len(acts)}")
if acts:
    first = acts[0]
    print(first.celex_uri)
    print(first.title)
```

### Run the Example Script

The [repository](https://github.com/diegoglezsu/bulletin-fetcher/tree/main/scripts) includes an executable helper script:

```bash
python scripts/run_eurlex.py
```

And also a Jupyter Notebook: `scripts/run_eurlex.ipynb`.
