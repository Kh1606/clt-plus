"""
전국 공사/공단 — national agencies listed in Sheet1 "공사" section.

Skipped:
  물산업플랫폼 kwater.or.kr (XML-based / no HTML table)
  한국도로공사 ex.co.kr (jsessionid URL, session-based)
  LH 한국주택토지공사 (only 1 notice returned)
"""
from scrapers.base import SourceMeta
from scrapers._helpers.simple_table import make_scrape


def _entry(sub, page, url, **opts):
    src = SourceMeta(region="공사", sub_entity=sub, source_page=page, source_url=url)
    return src, make_scrape(src, **opts)


SCRAPERS = [
    # 농어촌공사 — 9is/krc CMS, title col 1
    _entry("농어촌공사", "공지사항",
           "https://www.ekr.or.kr/planweb/board/list.krc?contentUid=402880317cc0644a017cc0c22f2800f0&boardUid=402880317cc0644a017cc463cec202be&contentUid=402880317cc0644a017cc0c22f2800f0&subPath=",
           require="view.krc"),
]
