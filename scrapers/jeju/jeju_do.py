"""
제주도청 고시 공고 — jeju.go.kr/news/news/law/jeju.htm

Same citynet template as 인천시청: row-level <tr onclick="viewData('66237','A')">
with no <a> on the title cell. The form action JS uses sido='' (empty).
Detail URL synthesized as a same-origin /citynet path.
"""
from __future__ import annotations
import re

from scrapers.base import Notice, SourceMeta, get, soup, parse_date, clean

SOURCE = SourceMeta(
    region="제주도",
    sub_entity="제주도청",
    source_page="고시 공고",
    source_url="http://www.jeju.go.kr/news/news/law/jeju.htm",
)
DETAIL_FMT = (
    "http://www.jeju.go.kr/citynet/jsp/sap/SAPGosiBizProcess.do"
    "?command=searchDetail&flag=gosiGL&svp=Y&sido=&sno={sno}&gosiGbn={gbn}"
)
_VIEW_RE = re.compile(r"viewData\([\'\"](\d+)[\'\"]\s*,\s*[\'\"]([A-Z])[\'\"]\)")


def _is_listing(table) -> bool:
    head = table.find("tr")
    if not head:
        return False
    head_text = head.get_text(" ", strip=True)
    return "고시" in head_text and "제목" in head_text and ("게재일자" in head_text or "게재일" in head_text)


def scrape() -> list[Notice]:
    r = get(SOURCE.source_url)
    s = soup(r.content)
    table = next((t for t in s.find_all("table") if _is_listing(t)), None)
    if not table:
        return []
    notices: list[Notice] = []
    body = table.find("tbody") or table
    for tr in body.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 4:
            continue
        m = _VIEW_RE.search(tr.get("onclick") or "")
        if not m:
            continue
        title = clean(tds[1].get_text())
        if not title:
            continue
        detail_url = DETAIL_FMT.format(sno=m.group(1), gbn=m.group(2))
        posted_at = parse_date(tds[3].get_text())
        notices.append(Notice(
            region=SOURCE.region, sub_entity=SOURCE.sub_entity,
            source_page=SOURCE.source_page, source_url=SOURCE.source_url,
            detail_url=detail_url, title=title, posted_at=posted_at,
        ))
    return notices
