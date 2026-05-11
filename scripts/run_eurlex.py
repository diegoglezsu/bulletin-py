"""Small script to query EUR-Lex acts using bulletin-fetcher."""

from sqlite3 import Date
import sys

from bulletin.eurlex.api.client import EurlexBulletinClient


def main() -> int:

    client = EurlexBulletinClient()

    date = "2025-01-01"
    date_end = "2026-03-31"
    title_contains = "science"
    category_type = "ANNOUNC"
    institution_type = "COM"
    language = "ENG"
    # Examples of filtering:
    # - Pass category_type="ANNOUNC" to filter by category type (e.g., announcements)
    # - Pass institution_type="COM" to filter by institution type (e.g., European Commission)

    try:
        acts = client.get_acts(
            date=date,
            date_end=date_end,
            language=language,
            title_contains=title_contains,
            category_type=category_type,
            institution_type=institution_type,
        )
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

    if acts:
        first_act = acts[0]
        print("\n" + "=" * 60 + "\n")
        print("Fetching content for the first act:")
        print(first_act.celex_uri)

        try:
            content = client.get_act_content(
                "52025M12135",
                language=language,
                max_size=500_000,
            )
        except Exception as exc:
            print(f"Error while fetching act content: {exc}", file=sys.stderr)
        else:
            print(content)

    print("\n" + "=" * 60 + "\n")

    formats = ["objects", "json", "csv", "xml", "df"]

    for fmt in formats:
        print(f"Testing output format: {fmt}")
        output = client.get_acts(
            date=date,
            date_end=date_end,
            title_contains=title_contains,
            language=language,
            category_type=category_type,
            institution_type=institution_type,
            output_format=fmt,
        )
        print(output)
        print("-" * 60)

    today_acts = client.get_acts(date=Date.today().isoformat())
    print(f"Acts published on {Date.today().isoformat()}: {len(today_acts)}")
    for act in today_acts:
        print(f"- {act.title} ({act.date}) {act.institution_label}")
    print("Today documents can be checked at https://eur-lex.europa.eu/oj/direct-access.html")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
