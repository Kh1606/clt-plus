"""
전라남도 — batch of sites using the simple_table helper.

Skipped:
  전남개발공사 (empty response)
  영산강유역환경청 me.go.kr (blocked)
  담양군 (JS-rendered / no links)
  곡성군 고시공고 (JS onclick only)
  구례군 고시공고 (JavaScript:searchDetail)
  고흥군, 함평군 (no table)
  영암군, 신안군 고시공고 (connection timeout)

Col layout note:
  Most custom CMS boards: 번호 | 제목 | 담당 | 날짜 | 조회 → col=1
  고시공고 boards often add 고시번호 column: 번호 | 고시번호 | 제목 | ... → col=2
"""
from scrapers.base import SourceMeta
from scrapers._helpers.simple_table import make_scrape


def _entry(sub, page, url, **opts):
    src = SourceMeta(region="전라남도", sub_entity=sub, source_page=page, source_url=url)
    return src, make_scrape(src, **opts)


SCRAPERS = [
    # 목포시 공지사항 — custom CMS, mode=view detail links, title col 1
    _entry("목포시", "공지사항",
           "https://www.mokpo.go.kr/www/mokpo_news/notice",
           require="mode=view"),
    # 목포시 고시공고 — same CMS, title col 1
    _entry("목포시", "고시공고",
           "https://www.mokpo.go.kr/www/mokpo_news/notification/public_notice",
           require="mode=view"),
    # 전남도청 공지사항 + 도로교통과 — boardView.do detail links, title col 1
    _entry("전남도청", "공지사항",
           "https://www.jeonnam.go.kr/J0203/boardList.do?menuId=jeonnam0203000000",
           require="boardView.do"),
    _entry("전남도청 도로교통과", "자료실",
           "https://www.jeonnam.go.kr/T8409/boardList.do?menuId=jeonnam0915020300",
           require="boardView.do"),
    # 여수시 — custom CMS, mode=view detail links
    _entry("여수시", "공지사항",
           "https://www.yeosu.go.kr/www/govt/news/notice",
           require="mode=view"),
    _entry("여수시", "고시공고",
           "https://www.yeosu.go.kr/www/govt/news/notify",
           title_col=2, require="mode=view"),
    # 순천시 — custom CMS, mode=view detail links
    _entry("순천시", "공지사항",
           "https://www.suncheon.go.kr/kr/news/0001/0001/",
           require="mode=view"),
    _entry("순천시", "고시공고",
           "http://www.suncheon.go.kr/kr/news/0004/0005/0002/",
           title_col=2, require="mode=view"),
    # 나주시 — custom CMS, mode=view
    _entry("나주시", "공지사항",
           "https://www.naju.go.kr/www/administration/new/notify",
           require="mode=view"),
    # 나주시 고시공고 — same CMS, col 2 (번호|고시공고번호|제목)
    _entry("나주시", "고시공고",
           "https://www.naju.go.kr/www/administration/notice/gosi_new",
           title_col=2, require="mode=view"),
    # 광양시 공지사항 — board.es ESMS, act=view detail links, title col 1
    _entry("광양시", "공지사항",
           "https://gwangyang.go.kr/board.es?mid=a11001000000&bid=0001",
           require="act=view"),
    # 광양시 고시공고 — saeol gosi.es, col 2 (번호|공고번호|제목)
    _entry("광양시", "고시공고",
           "https://gwangyang.go.kr/saeol/gosi.es?mid=a11005020000&type_code=02,04",
           title_col=2, require="act=view"),
    # 곡성군 공지사항 — eGovFrame board/view.do, title col 1
    _entry("곡성군", "공지사항",
           "https://www.gokseong.go.kr/kr/board/list.do?bbsId=BBS_000000000000150&menuNo=102001001000",
           require="view.do"),
    # 구례군 공지사항 — eGovFrame board/view.do, title col 1
    _entry("구례군", "공지사항",
           "https://www.gurye.go.kr/board/list.do?bbsId=BBS_0000000000000056&menuNo=115004001000",
           require="view.do"),
    # 보성군 — custom CMS, mode=view, title col 1
    _entry("보성군", "공지사항",
           "https://www.boseong.go.kr/www/open_administration/city_news/notice",
           require="mode=view"),
    _entry("보성군", "고시공고",
           "https://www.boseong.go.kr/www/open_administration/city_news/notification",
           require="mode=view"),
    # 화순군 — board.do ESMS variant, act=view, title col 1
    _entry("화순군", "공지사항",
           "https://www.hwasun.go.kr/board.do?S=S01&M=020102000000&b_code=0000000002",
           require="act=view"),
    # 장흥군 — custom CMS, mode=view
    _entry("장흥군", "공지사항",
           "https://www.jangheung.go.kr/www/organization/news/notice",
           require="mode=view"),
    _entry("장흥군", "고시공고",
           "https://www.jangheung.go.kr/www/organization/news/notification",
           title_col=2, require="mode=view"),
    # 강진군 — custom CMS, mode=view
    _entry("강진군", "공지사항",
           "https://www.gangjin.go.kr/www/government/news/notice",
           require="mode=view"),
    # 강진군 고시공고 — same CMS, title col 1 (번호|제목)
    _entry("강진군", "고시공고",
           "https://www.gangjin.go.kr/www/government/notice/gosi",
           require="mode=view"),
    # 해남군 공지사항 — 9is CMS, title col 1
    _entry("해남군", "공지사항",
           "https://www.haenam.go.kr/planweb/board/list.9is?contentUid=18e3368f5d745106015de95ebe732057&boardUid=18e3368f5fb80fdc015fdc42b7e003e0",
           require="view.9is"),
    # 영암군 공지사항 — custom CMS, show/ detail paths, title col 1
    _entry("영암군", "공지사항",
           "https://www.yeongam.go.kr/home/www/open_information/yeongam_news/notice",
           require="show/"),
    # 무안군 — custom CMS, mode=view, title col 1
    _entry("무안군", "공지사항",
           "https://www.muan.go.kr/www/openmuan/new/notice",
           require="mode=view"),
    _entry("무안군", "고시공고",
           "https://www.muan.go.kr/www/openmuan/new/announcement",
           require="mode=view"),
    # 영광군 — custom BBS, type=view detail links
    _entry("영광군", "공지사항",
           "https://www.yeonggwang.go.kr/bbs/?b_id=news_notice&site=headquarter_new&mn=9054",
           require="type=view"),
    _entry("영광군", "고시공고",
           "https://www.yeonggwang.go.kr/bbs/?b_id=gosigonggo&site=headquarter_new&mn=9059",
           title_col=2, require="type=view"),
    # 장성군 — custom CMS, show/ detail paths
    _entry("장성군", "공지사항",
           "https://www.jangseong.go.kr/home/www/news/jangseong/notice",
           require="show/"),
    _entry("장성군", "고시공고",
           "https://www.jangseong.go.kr/home/www/news/jangseong/announcement",
           title_col=2, require="show/"),
    # 진도군 — custom CS board
    _entry("진도군", "공지사항",
           "https://www.jindo.go.kr/home/board/B0052.cs?m=23",
           title_col=2, require="act=read"),
    _entry("진도군", "고시공고",
           "https://www.jindo.go.kr/home/gosi/general.cs?m=24",
           title_col=2, require="act=view"),
    # 완도군 — custom .cs board; nttId= distinguishes detail from list/page links
    _entry("완도군", "공지사항",
           "https://www.wando.go.kr/wando/sub.cs?m=298",
           require="nttId="),
    # 완도군 고시공고 — same site, col 2 (번호|고시공고번호|제목)
    _entry("완도군", "고시공고",
           "https://www.wando.go.kr/wando/sub.cs?m=318",
           title_col=2, require="nttId="),
    # 신안군 공지사항 — custom CMS, show/ detail paths, title col 1
    _entry("신안군", "공지사항",
           "https://www.shinan.go.kr/home/www/openinfo/participation_07/participation_07_02",
           require="show/"),
]
