#!/usr/bin/env python3
"""Turn a Goodreads reading-log export into _data/reading_log.csv for the site.

Usage:
    python3 scripts/build_reading_log.py path/to/goodreads_reading_log.csv

Reads the columns Title, Author, Date Read, Book Id and writes
_data/reading_log.csv with the columns: year, date, title, author.

- Rows are sorted newest to oldest. Re-reads that have their own dated row are
  kept as separate entries (it is a log).
- Titles are shortened for display: a trailing "(series, #n)" is dropped, and
  anything after the first ": " (the subtitle) is dropped.
- Authors have stray double spaces collapsed.
- Books with no read date go in a final "Pre-2016" group (the Goodreads log
  starts in 2016, so undated books are treated as read before that). An undated row is
  skipped when the same Book Id already has a dated row (Goodreads lists some
  re-read books twice).
"""
import csv
import re
import sys
from pathlib import Path


def clean_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    title = re.sub(r"\s*\([^()]*\)\s*$", "", title)  # trailing "(Series, #1)"
    title = title.split(": ", 1)[0]  # drop subtitle
    return title.strip()


def clean_author(author: str) -> str:
    return re.sub(r"\s+", " ", author).strip()


def main(src: str) -> None:
    with open(src, newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("Title")]

    dated, undated = [], []
    for r in rows:
        raw = (r.get("Date Read") or "").strip()
        entry = {
            "book_id": r["Book Id"],
            "title": clean_title(r["Title"]),
            "author": clean_author(r["Author"]),
            "date": raw.replace("/", "-"),
        }
        (dated if raw else undated).append(entry)

    dated.sort(key=lambda e: e["date"], reverse=True)
    dated_ids = {e["book_id"] for e in dated}
    seen_undated = set()
    undated_kept = []
    for e in sorted(undated, key=lambda e: e["title"].lower()):
        if e["book_id"] in dated_ids or e["book_id"] in seen_undated:
            continue
        seen_undated.add(e["book_id"])
        undated_kept.append(e)

    out = Path("_data")
    out.mkdir(exist_ok=True)
    with open(out / "reading_log.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "date", "title", "author"])
        for e in dated:
            w.writerow([e["date"][:4], e["date"], e["title"], e["author"]])
        for e in undated_kept:
            w.writerow(["Pre-2016", "", e["title"], e["author"]])

    print(f"{len(dated)} dated, {len(undated_kept)} undated "
          f"({len(undated) - len(undated_kept)} undated duplicates skipped)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
