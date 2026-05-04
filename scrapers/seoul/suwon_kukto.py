"""
수원 국토관리사무소 공지사항 — molit.go.kr/srocm

Uses the shared molit JSP board parser.
"""
from scrapers.base import SourceMeta
from scrapers._helpers.molit_jsp import scrape_molit_jsp

SOURCE = SourceMeta(
    region="서울특별시",
    sub_entity="수원 국토관리사무소",
    source_page="공지사항",
    source_url="https://www.molit.go.kr/srocm/USR/BORD0201/m_19696/LST.jsp",
)


def scrape():
    return scrape_molit_jsp(SOURCE)


if __name__ == "__main__":
    for n in scrape():
        print(f"{n.posted_at}  {n.title}")
