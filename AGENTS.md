# Agent Instructions for `bulletin-py`

Welcome to the `bulletin-py` codebase. This file contains context, architectural decisions, and rules to follow when contributing to this project. 

## 1. Project Overview
`bulletin-py` is a Python library designed to search and manage official bulletins, primarily focusing on the **Official Journal of the European Union (DOUE)** via the EUR-Lex / Cellar SPARQL endpoint.

## 2. Architecture & Subpackages
The codebase follows a modular design, split by bulletin source. Currently, the main subpackage is `src/bulletin/doue/`.

### `doue` Subpackage Structure
- **`client.py`**: Contains `DoueBulletinClient`. This is the **public API** for users. It orchestrates the internal connector and parses responses.
- **`_connector.py`**: Contains `_DoueConnector`. This is an **internal, private module** (denoted by `_`) responsible for building SPARQL queries and executing HTTP requests using `requests`. Do not expose it to regular users.
- **`models.py`**: Contains `dataclasses` such as `DoueOfficialAct` to provide structured, typed returns instead of raw JSON.
- **`constants.py`**: Centralizes all configuration, URIs, and mappings (e.g., `LANGUAGE_CODE_MAP`, `EuLanguageCode`, and `DEFAULT_LANGUAGE`).
- **`exceptions.py`**: Defines a granular hierarchy of custom errors (`BulletinError`, `QueryError`, `EndpointError`, etc.).

## 3. Technology Stack & Guidelines
- **Python Version**: >= 3.7 (Note: we use modern typing like `typing.Literal`, `dataclasses`, and `|` union operators where safe/supported via `from __future__ import annotations`).
- **Dependencies**: 
  - Core: `requests`
  - Development tools: `pytest`, `black`, `flake8`, `mypy`.
- **Formatting**: `black` configurations are specified in `pyproject.toml`.
- **Public vs Private API**: 
  - Internal logic MUST be hidden using underscores (e.g., `_connector.py`, `_DoueConnector`). 
  - The public API is strictly controlled through `__all__` exports in `__init__.py` files.

## 4. Testing Conventions
- We use `pytest`. Tests mirror the `src/` directory structure under the `tests/` folder.
- **Unit Tests**: Should mock external services or test pure logic (like query building and date validations). Fixtures (e.g., `connector()`) are preferred over ad-hoc instantiations.
- **Integration Tests**: Tests that hit the real, live Cellar SPARQL endpoint MUST be decorated with `@pytest.mark.integration`. 
  - Example execution: `pytest -m integration`
  - The `integration` marker is registered in `pyproject.toml`.

## 5. Typical Workflows
- **Running tests**: `pytest tests/ -v -s`
- **Installing for dev**: `pip install -e .[dev]`

## 6. Pending Work (Roadmap)
- Implement `parse_results(response: dict) -> list[DoueOfficialAct]` in `models.py` to map the raw JSON bindings returned by SPARQL into our dataclass models.
