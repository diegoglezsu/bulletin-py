from dataclasses import dataclass
from datetime import date

@dataclass
class DoueOfficialAct:
    celex_uri: str               # e.g. "http://publications.europa.eu/resource/celex/32025R0001"
    act_number: str | None
    title: str
    date: date
    section_code: str | None     # "I", "II", ...
    subsection_code: str | None
    category_code: str | None
    category_uri: str | None
    category_label: str | None
    institution_code: str | None
    institution_uri: str | None
    institution_label: str | None

def parse_results(results: dict) -> list[DoueOfficialAct]:
    """Parse SPARQL results into a list of DoueOfficialAct objects."""
    acts = []
    for binding in results["results"]["bindings"]:
        act = DoueOfficialAct(
            celex_uri=binding["act"]["value"],
            act_number=binding["actNumber"]["value"] if "actNumber" in binding else None,
            title=binding["title"]["value"],
            date=date.fromisoformat(binding["date"]["value"]),
            section_code=binding["sectionCode"]["value"] if "sectionCode" in binding else None,
            subsection_code=binding["subsectionCode"]["value"] if "subsectionCode" in binding else None,
            category_code=binding["categoryCode"]["value"] if "categoryCode" in binding else None,
            category_uri=binding["categoryUri"]["value"] if "categoryUri" in binding else None,
            category_label=binding["categoryLabel"]["value"] if "categoryLabel" in binding else None,
            institution_code=binding["institutionCode"]["value"] if "institutionCode" in binding else None,
            institution_uri=binding["institutionUri"]["value"] if "institutionUri" in binding else None,
            institution_label=binding["institutionLabel"]["value"] if "institutionLabel" in binding else None,
        )
        acts.append(act)
    return acts