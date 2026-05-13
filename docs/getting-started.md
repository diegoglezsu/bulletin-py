# Getting Started

## Requirements

- Python 3.7+
- Internet access

## Installation

Install from PyPI:

```bash
pip install bulletin-fetcher
```

Install with all dependencies:

```bash
pip install bulletin-fetcher[all]
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

acts_json = client.get_acts(
    date="2025-01-01",
    date_end="2025-03-31",
    title_contains="artificial intelligence",
    language="ENG",
    output_format="json", # xml, csv, df
)

print(f"Total acts: {len(acts)}")
if acts:
    first = acts[0]
    print(first.celex_uri)
    print(first.title)

    first_content = client.get_act_content(
        first.celex_uri,
        language="ENG",
    )
    print(first_content[:500])

    content_from_celex_id = client.get_act_content(
        "52025M12135",
        language="ENG",
    )
    print(content_from_celex_id[:500])
```

### Run Example Scripts

The repository includes runnable scripts and notebooks with examples and use cases of the library. These scripts can be found in the [`scripts`](https://github.com/diegoglezsu/bulletin-fetcher/tree/main/scripts) directory.
