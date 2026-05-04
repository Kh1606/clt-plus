"""
전라북도 — batch of sites.

Skipped:
  전북개발공사 (SSL error)
  전북지방환경청 me.go.kr (blocked)
  익산지방국토관리청 BRD.jsp (returns 0 notices)
  익산시, 남원시, 순창군 (404)
  김제시, 완주군, 진안군, 장수군, 고창군 (non-table list layout)
  무주군, 군산시 고시공고, eminwon.*.go.kr OfrAction.do (JS or unverified)
  전북도청 고시/공고, 진안군 고시/공고, etc. (JS index.*.go.kr)
  부안군 고시/공고 (TABLE but no valid <a>)

molit 국토관리사무소 boards use scrape_molit_jsp helper (LST.jsp, auto-detects date col).
"""
from scrapers.base import SourceMeta
from scrapers._helpers.simple_table import make_scrape
from scrapers._helpers.molit_jsp import scrape_molit_jsp


def _entry(sub, page, url, **opts):
    src = SourceMeta(region="전라북도", sub_entity=sub, source_page=page, source_url=url)
    return src, make_scrape(src, **opts)


def _molit(sub, page, url):
    src = SourceMeta(region="전라북도", sub_entity=sub, source_page=page, source_url=url)
    return src, (lambda s=src: scrape_molit_jsp(s))


SCRAPERS = [
    # 전북도청 공지사항 — board/list.jeonbuk, title col 1
    _entry("전북도청", "공지사항",
           "https://www.jeonbuk.go.kr/board/list.jeonbuk?boardId=BBS_0000012&menuCd=DOM_000000103001002001&contentsSid=841&cpath=",
           require="view.jeonbuk"),
    # 새만금개발공사 — board.es ESMS, title col 1
    _entry("새만금개발공사", "고시 공고",
           "https://www.sdco.or.kr/board.es?mid=a10601020000&bid=0007",
           require="act=view"),
    # 전주시 새소식 — 9is CMS, title col 1
    _entry("전주시", "새소식",
           "https://www.jeonju.go.kr/planweb/board/list.9is?page=1&contentUid=ff8080818990c349018b041a87373953&boardUid=ff8080818990c349018b1dbaa78e4b41&subPath=",
           require="view.9is"),
    # 군산시 공지사항 — custom CMS, title col 1; detail path contains m140/view
    _entry("군산시", "공지사항",
           "https://www.gunsan.go.kr/main/m140",
           require="m140/view"),
    # 정읍시 공지사항 — board/list.jeongeup, title col 1
    _entry("정읍시", "공지사항",
           "https://www.jeongeup.go.kr/board/list.jeongeup?boardId=BBS_0000012&menuCd=DOM_000000101001001000&contentsSid=5&cpath=",
           require="view.jeongeup"),
    # 임실군 공지사항 — board/list.imsil, title col 1
    _entry("임실군", "공지사항",
           "https://www.imsil.go.kr/board/list.imsil?boardId=BBS_0000002&menuCd=DOM_000000103001001000&contentsSid=161&cpath=",
           require="view.imsil"),
    # 부안군 공지사항 — board/list.buan, title col 1
    _entry("부안군", "공지사항",
           "https://www.buan.go.kr/board/list.buan?boardId=BBS_0000053&menuCd=DOM_000000103001001000&contentsSid=687&cpath=",
           require="view.buan"),
    # molit 국토관리사무소 boards
    _molit("광주 국토관리사무소", "공지사항",
           "http://www.molit.go.kr/irocm/USR/BORD0201/m_19663/LST.jsp"),
    _molit("남원 국토관리사무소", "공지사항",
           "http://www.molit.go.kr/irocm/USR/BORD0201/m_19785/LST.jsp"),
    _molit("순천 국토관리사무소", "공지사항",
           "http://www.molit.go.kr/irocm/USR/BORD0201/m_19814/LST.jsp"),
    _molit("전주 국토관리사무소", "공지사항",
           "http://www.molit.go.kr/irocm/USR/BORD0201/m_19805/LST.jsp"),
]
