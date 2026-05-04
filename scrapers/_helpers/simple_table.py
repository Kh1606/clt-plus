"""
Generic table-listing scraper.

Most Korean gov board pages share the shape:

  <table>
    <thead><tr><th>번호</th><th>제목</th>...<th>등록일</th>...</tr></thead>
    <tbody>
      <tr>
        <td>...</td>
        <td><a href="…detail…">제목</a></td>
        ...
        <td>2026-05-04</td>
        ...
      </tr>
    </tbody>
  </table>

Differences across sites:
- title column index (usually 1, sometimes 2 when there's an extra category col)
- date column index (auto-detected by scanning all cells for a parseable date)
- detail-link form (relative href is overwhelmingly common)
- which <table> to pick when multiple exist (default: largest)

This helper absorbs all that with a small per-site config.
"""
from __future__ import annotations
from typing import Callable
from urllib.parse import urljoin

from scrapers.base import Notice, SourceMeta, get, soup, parse_date, clean


def scrape_simple_table(
    source: SourceMeta,
    *,
    title_col: int = 1,
    require: str | None = None,
    listing_picker: Callable | None = None,
) -> list[Notice]:
    """Scrape a notice listing.

    title_col      Which <td> holds the <a>title (default 1)
    require        Substring the detail href must contain to be considered a
                   real notice (filters out '#', '#view', search links, etc.)
    listing_picker Optional callable(list[Tag]) -> Tag to pick the right
                   <table> when several exist. Default: largest by row count.
    """
    r = get(source.source_url)
    s = soup(r.content)
    tables = s.find_all("table")
    if not tables:
        return []
    table = (listing_picker(tables) if listing_picker
             else max(tables, key=lambda t: len(t.find_all("tr"))))

    notices: list[Notice] = []
    body = table.find("tbody") or table
    for tr in body.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) <= title_col:
            continue
        a = tds[title_col].find("a", href=True)
        if not a:
            continue
        href = (a.get("href") or "").strip()
        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue
        if require and require not in href:
            continue
        title = clean(a.get_text())
        if not title:
            continue
        detail_url = urljoin(source.source_url, href)
        # Auto-detect date column: first parseable date in the row.
        posted_at = next(
            (parse_date(td.get_text()) for td in tds if parse_date(td.get_text())),
            None,
        )
        notices.append(
            Notice(
                region=source.region,
                sub_entity=source.sub_entity,
                source_page=source.source_page,
                source_url=source.source_url,
                detail_url=detail_url,
                title=title,
                posted_at=posted_at,
            )
        )
    return notices


def make_scrape(source: SourceMeta, **opts):
    """Returns a thunk `() -> list[Notice]` for batch SCRAPERS exports."""
    def _scrape():
        return scrape_simple_table(source, **opts)
    return _scrape
