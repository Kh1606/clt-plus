"""
전라북도 — batch of sites.

Skipped:
  전북개발공사 (SSL error)
  전북지방환경청 me.go.kr (blocked)
  익산지방국토관리청 BRD.jsp (returns 0 notices)
  익산시, 남원시 공지, 순창군 (404 or JS onclick)
  완주군 고시, 진안군 고시, 장수군, 고창군, 무주군 고시 (JS index.*.go.kr / NO TABLES)
  김제시 공지, 완주군 공지, 진안군 공지 (non-table list layout)
  군산시 고시공고, eminwon.*.go.kr OfrAction.do (JS or unverified)
  전북도청 고시/공고 (JS index.jeonbuk)

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
    # 전주시 고시공고 — 9is CMS, extra 구분/고시번호 cols → title col 3
    _entry("전주시", "고시공고",
           "https://www.jeonju.go.kr/planweb/board/list.9is?contentUid=ff8080818990c349018b041a879f395a&boardUid=9be517a7914528ce01930aa3ddc26cf0&contentUid=ff8080818990c349018b041a879f395a&subPath=",
           title_col=3, require="view.9is"),
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
    # 부안군 고시공고 — board/list.buan, title col 1
    _entry("부안군", "고시공고",
           "https://www.buan.go.kr/board/list.buan?boardId=BBS_0000054&menuCd=DOM_000000103001003000&contentsSid=84&cpath=",
           require="view.buan"),
    # 김제시 고시공고 — board/list.gimje, title col 1
    _entry("김제시", "고시공고",
           "https://www.gimje.go.kr/board/list.gimje?boardId=BBS_0000044&menuCd=DOM_000000104003000000&contentsSid=196&cpath=",
           require="view.gimje"),
    # 남원시 고시공고 — board/post/list.do, col 2 (번호|공고번호|제목)
    _entry("남원시", "고시공고",
           "https://www.namwon.go.kr/board/post/list.do?boardUid=ff8080818ea1fec5018ea24137680031&menuUid=ff8080818e3beff0018e4077131b007a&sort=registerDt,desc",
           title_col=2, require="post/view.do"),
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
