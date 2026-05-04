"""
부산광역시 — additional batch sources not covered by individual scrapers.

부산도시공사 — was marked 404 with old URL; board/list2.do is the working endpoint.
"""
from scrapers.base import SourceMeta
from scrapers._helpers.simple_table import make_scrape


def _entry(sub, page, url, **opts):
    src = SourceMeta(region="부산광역시", sub_entity=sub, source_page=page, source_url=url)
    return src, make_scrape(src, **opts)


SCRAPERS = [
    # 부산도시공사 — board/list2.do, title col 1; view.do?boardId= distinguishes detail
    _entry("부산도시공사", "공지사항",
           "https://www.bmc.busan.kr/board/list2.do?boardId=BBS_0000001&menuCd=DOM_000000101001001000&contentsSid=25&cpath=",
           require="view.do?boardId=BBS_0000001"),
]
