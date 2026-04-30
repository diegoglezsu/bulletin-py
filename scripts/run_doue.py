"""Small script to query DOUE acts using bulletin-fetcher."""

import sys

from bulletin.doue.api.client import DoueBulletinClient

def main() -> int:

    client = DoueBulletinClient()

    date = "2025-01-01"
    date_end = "2025-03-31"
    title_contains = "artificial intelligence"
    language = "ENG"
    #category_type = "ANNOUNC"

    try:
        acts = client.get_acts(date=date, language=language, date_end=date_end, title_contains=title_contains, category_type=None, institution_type=None)
    except Exception as exc:
        print(f"Error while fetching acts: {exc}", file=sys.stderr)
        return 1

    print("-" * 60)

    for act in acts:
        print(f"CELEX URI: {act.celex_uri}")
        print(f"Title: {act.title}")
        print(f"Date: {act.date}")
        if act.category_label:
            print(f"Category: {act.category_label}")
        if act.institution_label:
            print(f"Institution: {act.institution_label}")
        print("-" * 60)

    print(f"Total acts: {len(acts)}")
    print("Done.")

    print("\n" + "=" * 60 + "\n")

    # Get data in CSV
    csv_output = client.get_acts_csv(date=date, date_end=date_end, title_contains=title_contains, language=language) 
    print("CSV Output:")
    print(csv_output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
