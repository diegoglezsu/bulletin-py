import pytest
from unittest.mock import patch, MagicMock
import requests

from bulletin.doue.repository._connector import DoueConnector
from bulletin.doue.exceptions import QueryError, EndpointError


@pytest.fixture
def connector():
    return DoueConnector()


class TestBuildActsQuery:
    """Tests for build_acts_query method."""

    def test_valid_date(self, connector):
        """Test query building with a valid date and default language."""
        query = connector.build_acts_query("2024-01-01")
        assert 'FILTER(?date = "2024-01-01"^^xsd:date)' in query
        assert (
            "expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG>"
            in query
        )
        assert 'FILTER(LANG(?categoryLabel) = "en")' in query

    def test_custom_language(self, connector):
        """Test query building with a custom language code."""
        query = connector.build_acts_query("2024-01-01", language="ENG")
        assert (
            "expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG>"
            in query
        )
        assert 'FILTER(LANG(?categoryLabel) = "en")' in query

    def test_invalid_date(self, connector):
        """Test query building with invalid date format raises QueryError."""
        with pytest.raises(QueryError, match="Invalid date format"):
            connector.build_acts_query("20240101")

        with pytest.raises(QueryError, match="Invalid date format"):
            connector.build_acts_query("01-01-2024")

    def test_unsupported_language(self, connector):
        """Test query building with unsupported language raises QueryError."""
        with pytest.raises(QueryError, match="Unsupported language: 'XYZ'"):
            connector.build_acts_query("2024-01-01", language="XYZ")

    def test_date_range(self, connector):
        """Test query building with date range."""
        query = connector.build_acts_query(date="2024-01-01", date_end="2024-01-31")
        assert 'FILTER(?date >= "2024-01-01"^^xsd:date)' in query
        assert 'FILTER(?date <= "2024-01-31"^^xsd:date)' in query

    def test_title_contains(self, connector):
        """Test query building with title_contains filter."""
        query = connector.build_acts_query(
            date="2024-01-01", title_contains="regulation"
        )
        assert 'CONTAINS(LCASE(STR(?title)), LCASE("regulation"))' in query

    def test_category_type(self, connector):
        """Test query building with category_type filter."""
        query = connector.build_acts_query(date="2024-01-01", category_type="RES")
        assert 'FILTER(?categoryCode = "RES")' in query

    def test_invalid_category_type(self, connector):
        """Test that empty category_type raises QueryError."""
        with pytest.raises(QueryError, match="category_type filter cannot be empty"):
            connector.build_acts_query(date="2024-01-01", category_type="  ")

    def test_invalid_date_end_order(self, connector):
        """Test that date_end before date raises QueryError."""
        with pytest.raises(QueryError, match="date_end must be on or after date"):
            connector.build_acts_query(date="2024-01-10", date_end="2024-01-01")


class TestBuildCategoryTypesQuery:
    """Tests for build_category_types_query method."""

    def test_default_language(self, connector):
        """Test query building for category types with default language."""
        query = connector.build_category_types_query()
        assert "skos:Concept" in query
        assert "resource-type" in query
        assert 'FILTER(LANG(?label) = "en")' in query

    def test_spanish_language(self, connector):
        """Test query building for category types with Spanish language."""
        query = connector.build_category_types_query(language="SPA")
        assert 'FILTER(LANG(?label) = "es")' in query

class TestBuildInstitutionTypesQuery:
    """Tests for build_institution_types_query method."""

    def test_default_language(self, connector):
        """Test query building for institution types with default language."""
        query = connector.build_institution_types_query()
        assert "corporate-body" in query
        assert 'FILTER(LANG(?label) = "en")' in query
        assert "DISTINCT ?code ?label" in query

    def test_spanish_language(self, connector):
        """Test query building for institution types with Spanish language."""
        query = connector.build_institution_types_query(language="SPA")
        assert "corporate-body" in query
        assert 'FILTER(LANG(?label) = "es")' in query


class TestExecuteQuery:
    """Tests for execute_query method."""

    def test_http_error(self, connector):
        """Test that execute_query raises EndpointError on HTTP error."""
        query = "SELECT * WHERE { ?s ?p ?o } LIMIT 1"
        
        with patch("bulletin.doue.repository._connector.requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 400
            http_error = requests.exceptions.HTTPError("400 Client Error")
            http_error.response = mock_response
            mock_response.raise_for_status.side_effect = http_error
            mock_post.return_value = mock_response
            
            with pytest.raises(EndpointError) as exc_info:
                connector.execute_query(query)
            
            assert exc_info.value.status_code == 400
            assert "HTTP 400" in str(exc_info.value)

    def test_connection_error(self, connector):
        """Test that execute_query raises EndpointError on connection failure."""
        query = "SELECT * WHERE { ?s ?p ?o } LIMIT 1"
        
        with patch("bulletin.doue.repository._connector.requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.ConnectionError(
                "Failed to connect"
            )
            
            with pytest.raises(EndpointError) as exc_info:
                connector.execute_query(query)
            
            assert exc_info.value.status_code is None

    def test_timeout_error(self, connector):
        """Test that execute_query raises EndpointError on timeout."""
        query = "SELECT * WHERE { ?s ?p ?o } LIMIT 1"
        
        with patch("bulletin.doue.repository._connector.requests.post") as mock_post:
            mock_post.side_effect = requests.exceptions.Timeout(
                "Request timed out"
            )
            
            with pytest.raises(EndpointError) as exc_info:
                connector.execute_query(query)
            
            assert exc_info.value.status_code is None
            assert "Failed to reach SPARQL endpoint" in str(exc_info.value)

    def test_success(self, connector):
        """Test that execute_query successfully returns parsed JSON response."""
        query = "SELECT * WHERE { ?s ?p ?o } LIMIT 1"
        expected_response = {
            "head": {"vars": ["s", "p", "o"]},
            "results": {"bindings": []}
        }
        
        with patch("bulletin.doue.repository._connector.requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = expected_response
            mock_post.return_value = mock_response
            
            result = connector.execute_query(query)
            
            assert result == expected_response
            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args[1]
            assert call_kwargs["timeout"] == 300
            assert call_kwargs["headers"]["Accept"] == "application/sparql-results+json"


@pytest.mark.integration
class TestExecuteQueryIntegration:
    """Integration tests for execute_query method with live endpoint."""

    def test_live_endpoint(self, connector):
        """Integration test with actual EUR-Lex SPARQL endpoint.

        This verifies our query syntax is correct according to the live Cellar endpoint.
        Retrieves acts from 2024-05-15 (a known date).
        """
        query = connector.build_acts_query("2024-05-15", language="ENG")
        result = connector.execute_query(query)

        assert "head" in result
        assert "results" in result
        assert "bindings" in result["results"]

        acts = result["results"]["bindings"]
        assert len(acts) > 0

        act = acts[0]
        assert "act" in act
        assert "title" in act
        assert "date" in act

    def test_bad_syntax(self, connector):
        """Test that executing invalid SPARQL query raises EndpointError (HTTP 400)."""
        bad_query = "SELECT * WHERE { esto es un error de sintaxis }"

        with pytest.raises(EndpointError) as exc_info:
            connector.execute_query(bad_query)

        assert exc_info.value.status_code == 400
        assert "HTTP 400" in str(exc_info.value)

    def test_unreachable_endpoint(self):
        """Test that a bad endpoint URL raises EndpointError without a status code."""
        fake_connector = DoueConnector(endpoint="https://esto-no-existe.europa.eu/sparql")

        with pytest.raises(EndpointError) as exc_info:
            fake_connector.execute_query("SELECT * WHERE { ?s ?p ?o } LIMIT 1")

        assert exc_info.value.status_code is None
        assert "Failed to reach SPARQL endpoint" in str(exc_info.value)

    def test_timeout(self):
        """Test that a timeout raises EndpointError."""
        connector = DoueConnector(timeout=0.001)
        query = connector.build_acts_query("2024-05-15")

        with pytest.raises(EndpointError) as exc_info:
            connector.execute_query(query)

        assert exc_info.value.status_code is None
        assert "Failed to reach SPARQL endpoint" in str(exc_info.value)
