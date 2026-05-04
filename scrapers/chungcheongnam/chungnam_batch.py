"""
충청남도 — batch of sites using the simple_table helper.

Skipped (JS-rendered / no links / 404):
  충남개발공사 (no links)
  금강유역환경청 (blocked)
  충남도청 종합건설사업소 ddc.go.kr (동두천시 domain — data error)
  서산시 고시공고 (contents.do JS / no table)
  당진시 고시공고 (JS sub page / no links)
  논산시 고시공고 (no table)
  예산군 (only file-download hrefs, no article links)
  홍성군 (only file-download hrefs, no article links)
  보령시 고시공고, 서천군 고시공고 (no table)
  태안군 고시공고, 청양군 고시공고 (no table)
  공주시 공지사항 (view.do?nttId links are file buttons — title uses #view JS onclick)
"""
from scrapers.base import SourceMeta
from scrapers._helpers.simple_table import make_scrape


def _src(sub_entity, source_page, source_url):
    return SourceMeta(
        region="충청남도",
        sub_entity=sub_entity,
        source_page=source_page,
        source_url=source_url,
    )


def _entry(sub, page, url, **opts):
    src = _src(sub, page, url)
    return src, make_scrape(src, **opts)


SCRAPERS = [
    # 충남도청 고시공고 — eGovFrame board, title col 1; view.do?nttId detail links
    _entry("충남도청", "고시공고",
           "https://www.chungnam.go.kr/cnportal/bbs/B0000488/list.do?menuNo=5100288",
           require="view.do?nttId"),
    # 천안시 고시공고 — saeol CMS, col 2 (번호|고시공고번호|제목); view.do?notAncmtMgtNo
    _entry("천안시", "고시공고",
           "https://www.cheonan.go.kr/prog/saeolGosi/GOSI/kor/sub02_02_01/list.do",
           title_col=2, require="view.do?notAncmtMgtNo"),
    # 금산군 공지사항 — custom HTML board, mode=V detail links, title col 1
    _entry("금산군", "공지사항",
           "https://www.geumsan.go.kr/kr/html/sub03/030101.html",
           require="mode=V"),
    # 금산군 고시공고 — same site, col 2 (번호|고시공고번호|제목)
    _entry("금산군", "고시공고",
           "https://www.geumsan.go.kr/kr/html/sub03/030302.html",
           title_col=2, require="mode=V"),
    # 부여군 고시공고 — same custom board as 공지사항, title col 1
    _entry("부여군", "고시공고",
           "https://www.buyeo.go.kr/_prog/_board/?code=news_02&site_dvs_cd=kr&menu_dvs_cd=040205",
           require="mode=V"),
    # 서산시 — eGovFrame selectBbsNttList, title col 1
    _entry("서산시", "공지사항",
           "https://www.seosan.go.kr/www/selectBbsNttList.do?bbsNo=97&key=1256",
           require="selectBbsNttView"),
    # 당진시 — eGovFrame selectBoardList, title col 1
    _entry("당진시", "공지사항",
           "https://www.dangjin.go.kr/cop/bbs/BBSMSTR_000000000013/selectBoardList.do",
           require="selectBoardArticle"),
    # 논산시 — custom CMS, mode=V detail links, title col 1
    _entry("논산시", "공지사항",
           "https://www.nonsan.go.kr/kor/html/sub03/030101.html",
           require="mode=V"),
    # 보령시 — eGovFrame selectBoardList, title col 1
    _entry("보령시", "공지사항",
           "https://www.brcn.go.kr/cop/bbs/BBSMSTR_000000000263/selectBoardList.do",
           require="selectBoardArticle"),
    # 부여군 — custom board, mode=V detail links, title col 1
    _entry("부여군", "공지사항",
           "https://www.buyeo.go.kr/_prog/_board/?code=news_01&site_dvs_cd=kr&menu_dvs_cd=0401",
           require="mode=V"),
    # 태안군 — eGovFrame selectBoardList, title col 1
    _entry("태안군", "공지사항",
           "https://www.taean.go.kr/cop/bbs/BBSMSTR_000000000036/selectBoardList.do",
           require="selectBoardArticle"),
    # 서천군 — eGovFrame selectBoardList, title col 1
    _entry("서천군", "공지사항",
           "https://www.seocheon.go.kr/cop/bbs/BBSMSTR_000000000056/selectBoardList.do",
           require="selectBoardArticle"),
    # 계룡시 공지사항 — custom CMS, mode=V, title col 1
    _entry("계룡시", "공지사항",
           "https://www.gyeryong.go.kr/kr/html/sub03/030101.html",
           require="mode=V"),
    # 계룡시 고시공고 — same CMS, title at col 2 (번호 / 고시번호 / 제목 ...)
    _entry("계룡시", "고시공고",
           "https://www.gyeryong.go.kr/kr/html/sub03/030102.html",
           title_col=2, require="mode=V"),
    # 청양군 — eGovFrame selectBoardList, title col 1
    _entry("청양군", "공지사항",
           "http://www.cheongyang.go.kr/cop/bbs/BBSMSTR_000000000037/selectBoardList.do",
           require="selectBoardArticle"),
]
