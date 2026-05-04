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
import os
import sys
import urllib3

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from scrapers.base import StdoutSink, JsonFileSink, SupabaseSink, polite_sleep

# Register scrapers here. Each entry is the dotted module path; the module
# must expose `SOURCE: SourceMeta` and `scrape() -> list[Notice]`.
SCRAPERS = [
    # 충청남도
    "scrapers.chungcheongnam.asan",
    "scrapers.chungcheongnam.chungnam_batch",
    # 충청북도
    "scrapers.chungcheongbuk.chungbuk_batch",
    # 경기도
    "scrapers.gyeonggi.gyeonggi_batch",
    # 전라북도
    "scrapers.jeonbuk.jeonbuk_batch",
    # 전라남도
    "scrapers.jeonnam.jeonnam_batch",
    # 대전광역시
    "scrapers.daejeon.daejeon_si",
    # 서울특별시 (5 of 8 — molit/env-ministry endpoints block bare requests)
    "scrapers.seoul.seoul_si",
    "scrapers.seoul.suwon_kukto",
    "scrapers.seoul.sisul",
    "scrapers.seoul.ish",
    "scrapers.seoul.doro_seoul",
    # 부산광역시 (7 of 10 — 부산지방국토관리청, 진영 국토관리사무소, 부산도시공사 fail/404)
    "scrapers.busan.busan_si",
    "scrapers.busan.jinju_kukto",
    "scrapers.busan.daegu_kukto",
    "scrapers.busan.pohang_kukto",
    "scrapers.busan.yeongju_kukto",
    "scrapers.busan.busan_gunsul",
    "scrapers.busan.bisco",
    # 대구광역시 (1 of 5 — 대구시청 JS-loaded; 김천/상주시청 404; 대구지방환경청 blocked)
    "scrapers.daegu.daegu_dosi",
    # 인천광역시 (2 of 3 — 인천도시공사 returns HTTP 500)
    "scrapers.incheon.incheon_si",
    "scrapers.incheon.jonggeon",
    # 광주광역시 (1 of 3 — 광주시청 + 도시건설본부 are JS-loaded)
    "scrapers.gwangju.gmcc",
    # 대전광역시 — finishing the metro (8 of 8)
    "scrapers.daejeon.daejeon_kukto",
    "scrapers.daejeon.nonsan_kukto",
    "scrapers.daejeon.chungju_kukto",
    "scrapers.daejeon.boeun_kukto",
    "scrapers.daejeon.yesan_kukto",
    "scrapers.daejeon.daejeon_gunseol",
    "scrapers.daejeon.dcco",
    # 울산광역시 (2 of 2)
    "scrapers.ulsan.umca",
    "scrapers.ulsan.ulsan_si",
    # 세종특별시 (1 of 2 — 세종도시교통공사 has no tables, JS-loaded)
    "scrapers.sejong.sejong_si_notice",
    "scrapers.sejong.sejong_si_gosi",
    # 경상북도 (9 of 38 — most are JS-rendered portal/saeol or open_content)
    "scrapers.gyeongsangbuk.gyeongbuk_batch",
    # 경상남도 (9 of 32 — portal/saeol JS, .web NO TABLES, etc.)
    "scrapers.gyeongsangnam.gyeongnam_batch",
    # 강원도 (15 of 32 — SSL errors, timeouts, JS onclick)
    "scrapers.gangwon.gangwon_batch",
    # 제주도 (3 of 4 — 서귀포시청 returns empty initial HTML)
    "scrapers.jeju.jeju_do",
    "scrapers.jeju.jeju_si",
    "scrapers.jeju.jpdc",
]


def main():
    urllib3.disable_warnings()

    # Windows consoles default to cp949; force UTF-8 with replace fallback so
    # an unprintable emoji in a title can't crash the whole scraper.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="Write all notices to this JSON file")
    ap.add_argument("--only", help="Run only modules whose path contains this substring")
    ap.add_argument(
        "--supabase",
        action="store_true",
        help="Upsert into Supabase. Reads SUPABASE_URL + SUPABASE_SECRET_KEY from env (or .env).",
    )
    args = ap.parse_args()

    stdout_sink = StdoutSink()
    json_sink = JsonFileSink(args.out) if args.out else None
    supabase_sink = None
    if args.supabase:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_SECRET_KEY")
        if not url or not key:
            print("ERROR: --supabase requires SUPABASE_URL and SUPABASE_SECRET_KEY in env (.env)", file=sys.stderr)
            sys.exit(2)
        supabase_sink = SupabaseSink(url, key)

    total = 0
    failures: list[tuple[str, str]] = []

    for mod_path in SCRAPERS:
        if args.only and args.only not in mod_path:
            continue
        try:
            mod = importlib.import_module(mod_path)
        except Exception as e:  # noqa: BLE001
            print(f"   ✗ IMPORT FAILED {mod_path}: {type(e).__name__}: {e}", file=sys.stderr)
            failures.append((mod_path, repr(e)))
            continue

        # Batch modules export SCRAPERS = [(SourceMeta, scrape_fn), ...]
        # Standard modules export SOURCE + scrape()
        entries = mod.SCRAPERS if hasattr(mod, "SCRAPERS") else [(mod.SOURCE, mod.scrape)]

        for src, scrape_fn in entries:
            print(f"\n── {src.region} / {src.sub_entity} / {src.source_page}")
            print(f"   {src.source_url}")
            try:
                notices = scrape_fn()
                count = stdout_sink.write(notices)
                if json_sink:
                    json_sink.write(notices)
                if supabase_sink:
                    supabase_sink.write(notices)
                print(f"   → {count} notices")
                total += count
            except Exception as e:  # noqa: BLE001
                print(f"   ✗ FAILED: {type(e).__name__}: {e}", file=sys.stderr)
                failures.append((f"{mod_path}/{src.sub_entity}", repr(e)))
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
