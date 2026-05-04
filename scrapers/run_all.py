"""
Run every scraper, print a per-site summary, optionally write to a JSON snapshot.

Usage:
  python -m scrapers.run_all                       # stdout only
  python -m scrapers.run_all --out src/data/notices.json   # also write JSON

Phase 2 will replace `--out` with a SupabaseSink that pushes to the `notices` table.
"""
from __future__ import annotations

import argparse
import importlib
import sys
import urllib3

from scrapers.base import StdoutSink, JsonFileSink, polite_sleep

# Register scrapers here. Each entry is the dotted module path; the module
# must expose `SOURCE: SourceMeta` and `scrape() -> list[Notice]`.
SCRAPERS = [
    "scrapers.chungcheongnam.asan",
    "scrapers.busan.busan_si",
    "scrapers.seoul.seoul_si",
    "scrapers.daejeon.daejeon_si",
]


def main():
    urllib3.disable_warnings()

    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="Write all notices to this JSON file")
    ap.add_argument("--only", help="Run only modules whose path contains this substring")
    args = ap.parse_args()

    stdout_sink = StdoutSink()
    json_sink = JsonFileSink(args.out) if args.out else None

    total = 0
    failures: list[tuple[str, str]] = []

    for mod_path in SCRAPERS:
        if args.only and args.only not in mod_path:
            continue
        try:
            mod = importlib.import_module(mod_path)
            src = mod.SOURCE
            print(f"\n── {src.region} / {src.sub_entity} / {src.source_page}")
            print(f"   {src.source_url}")
            notices = mod.scrape()
            count = stdout_sink.write(notices)
            if json_sink:
                json_sink.write(notices)
            print(f"   → {count} notices")
            total += count
        except Exception as e:  # noqa: BLE001
            print(f"   ✗ FAILED: {type(e).__name__}: {e}", file=sys.stderr)
            failures.append((mod_path, repr(e)))
        polite_sleep(1.0)

    if json_sink:
        json_sink.flush()
        print(f"\nWrote snapshot → {args.out}")

    print(f"\nTotal notices: {total}")
    if failures:
        print(f"Failures: {len(failures)}")
        for path, err in failures:
            print(f"  {path}  {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
