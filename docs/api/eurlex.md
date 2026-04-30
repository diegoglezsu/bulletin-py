# bulletin.eurlex

EUR-Lex support is split into two layers:

- API layer: high-level client and typed parsing models.
- Repository layer: connector for query construction and endpoint communication.
- [Official SPARQL Query Editor](https://publications.europa.eu/webapi/rdf/sparql)

## Basic Imports

```python
from bulletin.eurlex.api.client import EurlexBulletinClient
from bulletin.eurlex.api.models import EurlexOfficialAct
```

## Client

::: bulletin.eurlex.api.client.EurlexBulletinClient
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true

## Models

::: bulletin.eurlex.api.models.EurlexOfficialAct
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true

::: bulletin.eurlex.api.models.CategoryType
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true

::: bulletin.eurlex.api.models.InstitutionType
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true

## Constants

::: bulletin.eurlex.constants.LANGUAGE_CODE_MAP
    options:
      heading_level: 3
      show_root_heading: true
      show_root_toc_entry: true
