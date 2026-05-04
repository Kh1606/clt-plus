"""
경기도 — batch of sites using the simple_table helper.

Skipped (JS-rendered / SSL error / 404 / JS-onclick navigation):
  경기도청 (JS table, no anchors)
  성남시청, 안양시청, 용인시청 공법 (SSL errors)
  고양시청, 남양주시청, 수원시청, 안산시청, 화성시청, 양주시, 의왕시 (JS/no table)
  용인시청 입찰 (JSP session-based)
  평택시청 (404)
  시흥시청, 의정부시청, 과천시, 광명시, 광주시, 안성시, 오산시, 이천시 (saeol CMS — title anchors use req.post/boardView JS)
  파주시 (BD_board — title anchors use jsView JS)

selectGosiList.do col layout: 번호 | 고시번호 | [날짜 or 분류] | 제목 | 담당 | 기간
selectGosiNttList.do col layout: 번호 | 고시번호 | 제목 | 담당 | 날짜
selectEminwonList.do col layout varies: col 1 (포천) or col 2 (군포)
"""
from scrapers.base import SourceMeta
from scrapers._helpers.simple_table import make_scrape


def _entry(sub, page, url, **opts):
    src = SourceMeta(region="경기도", sub_entity=sub, source_page=page, source_url=url)
    return src, make_scrape(src, **opts)


SCRAPERS = [
    # 경기도시공사 — article board, col 1
    _entry("경기도시공사", "고시 공고",
           "https://www.gh.or.kr/gh/bid-announcement.do",
           require="mode=view"),
    # 부천시청 — basicboard, col 1; encid= distinguishes detail from list
    _entry("부천시청", "기타공고",
           "https://www.bucheon.go.kr/site/program/board/basicboard/list?boardtypeid=26754&menuid=148002003002",
           require="encid="),
    # 가평군 — selectGosiList, col 3 (번호|고시번호|날짜|제목|담당|기간)
    _entry("가평군", "고시 공고",
           "https://www.gp.go.kr/portal/selectGosiList.do?key=2148&not_ancmt_se_code=01",
           title_col=3, require="selectGosiData"),
    # 구리시 — selectGosiNttList, col 2 (번호|고시번호|제목|담당|날짜)
    _entry("구리시", "고시 공고",
           "https://www.guri.go.kr/www/selectGosiNttList.do?key=387&searchGosiSe=01,04,06",
           title_col=2, require="selectGosiNttView"),
    # 군포시 — selectEminwonList, col 2
    _entry("군포시", "고시 공고",
           "http://www.gunpo.go.kr/www/selectEminwonList.do?key=3907&Not_ancmt_se_code=01,04&list_gubun=N&ofr_pageSize=10",
           title_col=2, require="selectEminwonView"),
    # 동두천시 — selectGosiList, col 2 (번호|고시번호|제목|담당|날짜)
    _entry("동두천시", "고시 공고",
           "https://www.ddc.go.kr/ddc/selectGosiList.do?key=340&not_ancmt_se_code=04",
           title_col=2, require="selectGosiData"),
    # 김포시 — ntfcPblancList, col 2 (번호|고시번호|제목|담당|날짜)
    _entry("김포시", "고시 공고",
           "https://www.gimpo.go.kr/portal/ntfcPblancList.do?key=1004&cate_cd=1&searchCnd=40900000000",
           title_col=2, require="ntfcPblancView"),
    # 양평군 — selectBbsNttList, col 1
    _entry("양평군", "고시 공고",
           "https://www.yp21.go.kr/www/selectBbsNttList.do?bbsNo=5&key=1119",
           require="selectBbsNttView"),
    # 여주시 — selectBbsNttList, col 3 (번호|고시번호|분류|제목|첨부|담당|날짜|조회)
    _entry("여주시", "공고 공시 입법예고",
           "https://www.yeoju.go.kr/www/selectBbsNttList.do?bbsNo=28&key=354",
           title_col=3, require="selectBbsNttView"),
    # 연천군 — selectGosiList, col 3 (번호|고시번호|날짜|제목|담당|기간)
    _entry("연천군", "고시 공고",
           "https://www.yeoncheon.go.kr/www/selectGosiList.do?key=3393&not_ancmt_se_code=01",
           title_col=3, require="selectGosiData"),
    # 포천시 — selectEminwonList, col 1 (번호|제목|담당|날짜)
    _entry("포천시", "고시 공고",
           "https://www.pocheon.go.kr/www/selectEminwonList.do?key=12563&notAncmtSeCode=01",
           require="selectEminwonView"),
    # 하남시 — selectGosiList, col 3 (번호|고시번호|날짜|제목|담당|기간)
    _entry("하남시", "고시 공고",
           "https://www.hanam.go.kr/www/selectGosiList.do?key=171&not_ancmt_se_code=01,03,04",
           title_col=3, require="selectGosiData"),
]
