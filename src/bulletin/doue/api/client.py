"""
High-level client for querying EU Official Journal (DOUE) acts.
"""

from ..repository._connector import DoueConnector
from ..constants import DEFAULT_LANGUAGE, SPARQL_ENDPOINT
from ..converters import acts_to_csv, parse_acts_results, parse_category_types_results, parse_institution_types_results
from .models import DoueOfficialAct, CategoryType, InstitutionType


class DoueBulletinClient:
    """Client to query EU Official Journal acts."""

    def __init__(self, endpoint: str = SPARQL_ENDPOINT, timeout: int = 300):
        self._connector = DoueConnector(endpoint=endpoint, timeout=timeout)

    def get_acts(
        self, date: str, language: str = DEFAULT_LANGUAGE, date_end: str | None = None, title_contains: str | None = None, category_type: str | None = None
    ) -> list[DoueOfficialAct]:
        """Fetch Official Journal acts for a given publication date.

        Args:
            date: Publication date in ISO format (e.g. "2025-03-27").
            date_end: End date in ISO format (e.g. "2025-03-27"). If provided, fetch acts published between `date` and `date_end` inclusive.
            title_contains: Case-insensitive substring filter on title.
            category_type: Filter by category type code (e.g. "RES" for Resolution). Optional.
            language: Language code (default: "ENG"). Supported values are defined in `LANGUAGE_CODE_MAP`. Examples: "ENG", "FRA", "DEU", "SPA"...

        Returns:
            A list of DoueOfficialAct objects.
        """
        query = self._connector.build_acts_query(date, language=language, date_end=date_end, title_contains=title_contains, category_type=category_type)
        response = self._connector.execute_query(query)
        return parse_acts_results(response)

    def get_acts_csv(self, date: str, date_end: str | None = None, title_contains: str | None = None, category_type: str | None = None, language: str = DEFAULT_LANGUAGE) -> str:
        """
        Fetch Official Journal acts for a given date and return CSV output.

        Args:
            date: Publication date in ISO format (e.g. "2025-03-27").
            date_end: End date in ISO format (e.g. "2025-03-27"). If provided, fetch acts published between `date` and `date_end` inclusive.
            title_contains: Case-insensitive substring filter on title.
            category_type: Filter by category type code (e.g. "RES" for Resolution). Optional.
            language: Language code (default: "ENG"). Supported values are defined in `LANGUAGE_CODE_MAP`. Example: "ENG", "FRA", "DEU", "SPA".
        Returns:
            A string containing the CSV representation of the acts.

        """
        acts = self.get_acts(date, language=language, date_end=date_end, title_contains=title_contains, category_type=category_type)
        return acts_to_csv(acts)

    def get_category_types(self, language: str = DEFAULT_LANGUAGE) -> list[CategoryType]:
        """Fetch the list of possible category types from the authority list. This method may last a few minutes due to the size of the authority list.

        Args:
            language: Language code (default: "ENG"). Examples: "ENG", "SPA", "FRA"...

        Returns:
            A list of CategoryType objects with 'code' and 'label' attributes.
        """
        query = self._connector.build_category_types_query(language=language)
        response = self._connector.execute_query(query)
        return parse_category_types_results(response)
    
    def get_institution_types(self, language: str = DEFAULT_LANGUAGE) -> list[InstitutionType]:
        """Fetch the list of possible institution types from the authority list. This method may last a few minutes due to the size of the authority list.

        Args:
            language: Language code (default: "ENG"). Examples: "ENG", "SPA", "FRA"...

        Returns:
            A list of InstitutionType objects with 'code' and 'label' attributes.
        """
        query = self._connector.build_institution_types_query(language=language)
        response = self._connector.execute_query(query)
        return parse_institution_types_results(response)
