"""
서울시설관리공단 알림마당 — sisul.or.kr/open_content/main/introduce/notice.jsp

Listing table columns: no / 제목 / 첨부 / 작성자 / 작성일 / 조회수
Detail link relative: /open_content/main/bbs/bbsMsgDetail.do?msg_seq=8739&bcd=notice
Date is at column index 4 (작성일).
"""
from __future__ import annotations
from urllib.parse import urljoin

from scrapers.base import Notice, SourceMeta, get, soup, parse_date, clean

SOURCE = SourceMeta(
    region="서울특별시",
    sub_entity="서울시설관리공단",
    source_page="알림마당",
    source_url="https://www.sisul.or.kr/open_content/main/introduce/notice.jsp",
)


def scrape() -> list[Notice]:
    r = get(SOURCE.source_url)
    s = soup(r.content)
    table = s.find("table")
    if not table:
        return []

    notices: list[Notice] = []
    body = table.find("tbody") or table
    for tr in body.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 5:
            continue
        a = tds[1].find("a")
        if not a:
            continue
        title = clean(a.get_text())
        detail_url = urljoin(SOURCE.source_url, a.get("href", ""))
        posted_at = parse_date(tds[4].get_text())
        if not title or "bbsMsgDetail" not in detail_url:
            continue
        notices.append(
            Notice(
                region=SOURCE.region,
                sub_entity=SOURCE.sub_entity,
                source_page=SOURCE.source_page,
                source_url=SOURCE.source_url,
                detail_url=detail_url,
                title=title,
                posted_at=posted_at,
            )
        )
    return notices


if __name__ == "__main__":
    for n in scrape():
        print(f"{n.posted_at}  {n.title}")
