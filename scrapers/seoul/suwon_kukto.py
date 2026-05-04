"""
수원 국토관리사무소 공지사항 — molit.go.kr/srocm/.../m_19696/LST.jsp

Same molit JSP base as the failing 서울지방국토관리청 endpoint, but THIS path
happens to respond. Listing table columns: 번호 / 제목 / 등록일자 / 담당부서 / 조회
Detail link is a relative href: ./DTL.jsp?id=scmo_0801_02_1&cate=&mode=view&idx=...
"""
from __future__ import annotations
from urllib.parse import urljoin

from scrapers.base import Notice, SourceMeta, get, soup, parse_date, clean

SOURCE = SourceMeta(
    region="서울특별시",
    sub_entity="수원 국토관리사무소",
    source_page="공지사항",
    source_url="https://www.molit.go.kr/srocm/USR/BORD0201/m_19696/LST.jsp",
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
        if len(tds) < 3:
            continue
        a = tds[1].find("a")
        if not a:
            continue
        title = clean(a.get_text())
        detail_url = urljoin(SOURCE.source_url, a.get("href", ""))
        posted_at = parse_date(tds[2].get_text())  # date is col 2 here
        if not title or "DTL" not in detail_url:
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
