"""
충청남도 — batch of sites using the simple_table helper.

Skipped (JS-rendered / timeout / 404):
  충남도청 고시공고 (board.do/JS)
  충남개발공사 (JS)
  금강유역환경청 (blocked)
  충남도청 종합건설사업소 (custom port 8100)
  천안시 (contents.do JS)
  아산시 고시공고 (handled by asan.py 공지사항; gosi uses same CMS but not verified)
  서산시 고시공고 (contents.do JS)
  당진시 고시공고 (custom sub page)
  논산시 고시공고 (no table)
  예산군 (no table)
  홍성군 (title anchors are JS-only #view)
  공주시 (title anchors are JS-only #view)
  금산군 (connection timeout)
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
