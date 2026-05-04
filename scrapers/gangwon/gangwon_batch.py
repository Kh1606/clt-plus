"""
강원도 — batch of sites.

Skipped (JS / SSL error / timeout / NO TABLES):
  춘천시×2 (NO TABLES), 홍천군 고시 (eminwon JS),
  화천군 고시 (contents.do NO TABLES),
  정선군×2 (only download hrefs / NO TABLES), 양구군×2 (user_sub.php NO TABLES),
  강릉시×2 (SSL handshake failure), 고성군×2 (SSL error),
  속초시×2 (SSL error), 동해시×2 (SSL error), 삼척시×2 (.web NO TABLES),
  양양군×2 (JS #a), 강원도청 고시+도로사업소 (href=#nolink JS)

molit 강릉/정선/홍천 국토관리사무소 — LST.jsp boards (molit_jsp helper).
평창군 고시 — portal CMS, noticeMgrNo param in detail hrefs, title col 1.
"""
from scrapers.base import SourceMeta
from scrapers._helpers.simple_table import make_scrape
from scrapers._helpers.molit_jsp import scrape_molit_jsp


def _entry(sub, page, url, **opts):
    src = SourceMeta(region="강원도", sub_entity=sub, source_page=page, source_url=url)
    return src, make_scrape(src, **opts)


def _molit(sub, page, url):
    src = SourceMeta(region="강원도", sub_entity=sub, source_page=page, source_url=url)
    return src, (lambda s=src: scrape_molit_jsp(s))


SCRAPERS = [
    # 원주시 — selectBbsNttList CMS; 공지 col 1, 고시 col 2
    _entry("원주시", "공지사항",
           "https://www.wonju.go.kr/www/selectBbsNttList.do?bbsNo=1&key=211&",
           require="selectBbsNttView"),
    _entry("원주시", "고시공고",
           "https://www.wonju.go.kr/www/selectBbsNttList.do?bbsNo=140&key=216&",
           title_col=2, require="selectBbsNttView"),
    # 홍천군 공지 — selectBbsNttList CMS, title col 1
    _entry("홍천군", "공지사항",
           "https://www.hongcheon.go.kr/www/selectBbsNttList.do?key=255&bbsNo=1",
           require="selectBbsNttView"),
    # 횡성군 공지 — selectBbsNttList CMS, title col 1
    _entry("횡성군", "공지사항",
           "https://www.hsg.go.kr/www/selectBbsNttList.do?bbsNo=59&key=812&",
           require="selectBbsNttView"),
    # 횡성군 고시 — same CMS (jsessionid in href), title col 1
    _entry("횡성군", "고시공고",
           "https://www.hsg.go.kr/www/selectBbsNttList.do?bbsNo=65&key=821&",
           require="selectBbsNttView"),
    # 영월군 — selectBbsNttList CMS; 공지 col 1, 고시 col 1 (고시번호 not separate)
    _entry("영월군", "공지사항",
           "https://www.yw.go.kr/www/selectBbsNttList.do?bbsNo=15&key=25",
           require="selectBbsNttView"),
    _entry("영월군", "고시공고",
           "https://www.yw.go.kr/www/selectBbsNttList.do?bbsNo=17&key=273",
           require="selectBbsNttView"),
    # 철원군 공지 — selectBbsNttList CMS (CWG_JSESSIONID in href), title col 1
    _entry("철원군", "공지사항",
           "https://www.cwg.go.kr/www/selectBbsNttList.do?bbsNo=24&key=206",
           require="selectBbsNttView"),
    # 철원군 고시 — same CMS, title col 1
    _entry("철원군", "고시공고",
           "https://www.cwg.go.kr/www/selectBbsNttList.do?bbsNo=25&key=1226",
           require="selectBbsNttView"),
    # 화천군 공지 — selectBbsNttList CMS, title col 1
    _entry("화천군", "공지사항",
           "https://www.ihc.go.kr/www/selectBbsNttList.do?bbsNo=11&key=2338",
           require="selectBbsNttView"),
    # 인제군 — portal/adm CMS, articleSeq detail links, title col 1
    _entry("인제군", "공지사항",
           "https://www.inje.go.kr/portal/adm/notice",
           require="articleSeq"),
    _entry("인제군", "고시공고",
           "https://www.inje.go.kr/portal/adm/bulletin/notify",
           require="articleSeq"),
    # 평창군 — portal CMS; 공지 articleSeq, 고시 noticeMgrNo
    _entry("평창군", "공지사항",
           "https://www.pc.go.kr/portal/government/government-news",
           require="articleSeq"),
    _entry("평창군", "고시공고",
           "https://www.pc.go.kr/portal/government/government-notification",
           require="noticeMgrNo"),
    # 태백시 — selectBbsNttList CMS, title col 1
    _entry("태백시", "공지사항",
           "https://www.taebaek.go.kr/www/selectBbsNttList.do?bbsNo=24&key=351",
           require="selectBbsNttView"),
    _entry("태백시", "고시공고",
           "https://www.taebaek.go.kr/www/selectBbsNttList.do?bbsNo=25&key=352",
           require="selectBbsNttView"),
    # molit 국토관리사무소 boards (LST.jsp)
    _molit("강릉 국토관리사무소", "공지사항",
           "http://www.molit.go.kr/wrocm/USR/BORD0201/m_20081/LST.jsp"),
    _molit("정선 국토관리사무소", "공지사항",
           "http://www.molit.go.kr/wrocm/USR/BORD0201/m_20143/LST.jsp"),
    _molit("홍천 국토관리사무소", "공지사항",
           "http://www.molit.go.kr/wrocm/USR/BORD0201/m_19978/LST.jsp"),
]
