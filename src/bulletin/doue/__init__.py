"""
DOUE (Diario Oficial de la Unión Europea) subpackage.

Provides tools to query official acts from the EU Official Journal
via the EUR-Lex / Cellar SPARQL endpoint.
"""

from .models import DoueOfficialAct
from .exceptions import BulletinError, QueryError, EndpointError

__all__ = [
    "DoueOfficialAct",
    "BulletinError",
    "QueryError",
    "EndpointError",
]
