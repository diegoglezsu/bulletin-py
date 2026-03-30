# Agent Instructions for `bulletin-fetcher`

Welcome to the `bulletin-fetcher` codebase. This file contains context, architectural decisions, and rules to follow when contributing to this project.

## 1. Project Overview

`bulletin-fetcher` is a Python library designed to search and manage official bulletins, primarily focusing on the **Official Journal of the European Union (DOUE)** via the EUR-Lex / Cellar SPARQL endpoint.

## 2. Architecture & Subpackages

The codebase follows a modular design, split by bulletin source. Currently, the main subpackage is `src/bulletin/doue/`.

### `doue` Subpackage Structure

- **`api/client.py`**: Contains `DoueBulletinClient`. This is the **public API** entrypoint for users. It orchestrates the connector and parsing layer.
- **`api/models.py`**: Contains `DoueOfficialAct` and `parse_results(...)` to map SPARQL JSON bindings into typed models.
- **`repository/_connector.py`**: Contains `DoueConnector`. This is the connector/data-access layer responsible for building SPARQL queries and executing HTTP requests.
- **`constants.py`**: Centralizes endpoint and language config (`SPARQL_ENDPOINT`, `LANGUAGE_CODE_MAP`, `SUPPORTED_LANGUAGE_CODES`, `DEFAULT_LANGUAGE`).
- **`exceptions.py`**: Defines custom errors (`BulletinError`, `QueryError`, `EndpointError`).
- **`__init__.py`**: Controls exports for `bulletin.doue` via `__all__`.

### Current Layering

- **Public API layer**: `bulletin.doue.api`
- **Repository layer**: `bulletin.doue.repository`
- **Root exports**: `bulletin.doue` currently exposes `api` and exception classes.

## 3. Technology Stack & Guidelines

- **Python Version**: >= 3.7
- **Dependencies**:
  - Core: `requests`
  - Development tools: `pytest`, `black`, `flake8`, `mypy`.
- **Formatting**: `black` configurations are specified in `pyproject.toml`.
- **Public vs Private API**:
  - Keep internals in repository/data-access modules and avoid exposing connector details through top-level package exports.
  - Private helper functions inside modules can use underscores (e.g., `_required_value`, `_optional_value`).
  - The public API is strictly controlled through `__all__` exports in `__init__.py` files.

## 4. Testing Conventions

- We use `pytest`. Tests mirror the `src/` directory structure under the `tests/` folder.
- **Unit Tests**: Should mock external services or test pure logic (like query building and date validations). Fixtures (e.g., `connector()`) are preferred over ad-hoc instantiations.
- **Integration Tests**: Tests that hit the real, live Cellar SPARQL endpoint MUST be decorated with `@pytest.mark.integration`.
  - Example execution: `pytest -m integration`
  - The `integration` marker is registered in `pyproject.toml`.

## 5. Typical Workflows

- **Running tests**: `pytest tests/ -v -s`
- **Running unit-only tests**: `pytest tests/doue -m "not integration"`
- **Installing for dev**: `pip install -e .[dev]`
- **Building package**: `python -m build`
- **Building docs**: `mkdocs build`

## 6. Pending Work (Roadmap)

- Keep this file synchronized with code structure changes (especially module paths and exported symbols).
- If public API exports change, update both docs (`docs/api/doue.md`) and tests import paths together.
