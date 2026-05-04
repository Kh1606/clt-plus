"""
경상북도 — batch of sites.

Skipped (JS-rendered / 404 / blocked):
  포항시×2, 경주시×2, 김천시×2, 구미시×2, 영주시×2, 영천시×2, 상주시×2,
  문경시×2, 경산시×2, 군위군×2, 의성군×2, 청송군×2, 청도군×2, 고령군×2,
  성주군×2, 칠곡군×2, 봉화군×2, 울진군 고시  (portal/saeol JS, open_content
  JS, .web NO TABLES, board/list.tc 404, open.content NO TABLES)

경북도청 — eGovFrame board, title col 1; detail href contains BD_CODE=gosi_notice
안동시 공지 — portal/bbs/list.do, direct view links, title col 1
안동시 고시 — portal/saeol/gosi/list.do, direct view links, title col 2
영양군, 영덕군 — custom CMS with mode= / mod=document detail paths
예천군 공지 — open.content CMS, ?i= detail links, title col 1
예천군 고시 — open.content CMS, ?id= detail links, title col 2
"""
from scrapers.base import SourceMeta
from scrapers._helpers.simple_table import make_scrape


def _entry(sub, page, url, **opts):
    src = SourceMeta(region="경상북도", sub_entity=sub, source_page=page, source_url=url)
    return src, make_scrape(src, **opts)


SCRAPERS = [
    # 경북도청 고시공고 — eGovFrame board, title col 1
    _entry("경북도청", "고시공고",
           "https://www.gb.go.kr/Main/page.do?mnu_uid=6789&&BD_CODE=gosi_notice",
           require="BD_CODE=gosi_notice"),
    # 안동시 — portal/bbs/list.do (공지) + portal/saeol/gosi (고시)
    _entry("안동시", "공지사항",
           "https://www.andong.go.kr/portal/bbs/list.do?ptIdx=156&mId=0401010000",
           require="portal/bbs/view.do"),
    _entry("안동시", "고시공고",
           "https://www.andong.go.kr/portal/saeol/gosi/list.do?mId=0401020100",
           title_col=2, require="portal/saeol/gosi/view.do"),
    # 영양군 — custom CMS, mode=view detail links, title col 1
    _entry("영양군", "공지사항",
           "https://www.yyg.go.kr/www/organization/yyg_news/notice",
           require="mode=view"),
    _entry("영양군", "고시공고",
           "https://www.yyg.go.kr/www/organization/yyg_news/notification",
           require="mode=view"),
    # 영덕군 — WordPress-style board, mod=document detail links, title col 1
    _entry("영덕군", "공지사항",
           "https://www.yd.go.kr/?page_id=752",
           require="mod=document"),
    _entry("영덕군", "고시공고",
           "https://www.yd.go.kr/?page_id=763",
           require="mod=document"),
    # 예천군 — open.content CMS: 공지 uses ?i= links (col 1), 고시 uses ?id= links (col 2)
    _entry("예천군", "공지사항",
           "https://www.ycg.kr/open.content/ko/administrative/news/notice/",
           require="./?i="),
    _entry("예천군", "고시공고",
           "https://www.ycg.kr/open.content/ko/administrative/news/announcement/",
           title_col=2, require="?id="),
]
