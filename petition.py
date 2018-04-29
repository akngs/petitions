from typing import Dict
from urllib import request
from urllib.error import HTTPError

from bs4 import BeautifulSoup


def main():
    latest_id = get_latest_article_id()
    next_id = get_latest_saved_article_id() + 1
    for i in range(next_id, latest_id):
        html = fetch_article(i)
        if html is None:
            continue
        parsed_article = parse_article(html)
        save_article(parsed_article)


def get_latest_article_id() -> int:
    """만료된 청원 목록 페이지를 분석하여 가장 최근에 만료된 글번호를 가져오기"""
    html = fetch_html('https://www1.president.go.kr/petitions?only=finished')
    soup = BeautifulSoup(html, "html5lib")
    elements = soup.select('.bl_body .bl_wrap .bl_no', limit=1)
    if len(elements) == 0:
        raise ValueError(f'Unable to find the latest article\'s id')
    return int(elements[0].text)


def get_latest_saved_article_id() -> int:
    """이미 저장한 가장 최근 글번호를 가져오기. 저장된 글이 없으면 0을 반환"""
    return 0


def fetch_article(article_id: int) -> str:
    """글번호에 해당하는 글의 HTML 텍스트를 가져오기. 해당 글이 없으면 ValueError"""
    raise ValueError(f'Not found: {article_id}')


def parse_article(html: str) -> Dict[str, any]:
    """본문 HTML에서 저장할 데이터를 추출하여 반환. 실패하면 ValueError"""
    raise ValueError('Failed to parse HTML')


def save_article(article: Dict[str, any]) -> None:
    """글을 CSV 형태로 저장한다"""
    pass


def fetch_html(url: str) -> str:
    try:
        with request.urlopen(url) as f:
            if f.getcode() != 200:
                raise ValueError(f'Invalid status code: {f.getcode()}')
            html = f.read().decode('utf-8')
            return html
    except HTTPError as e:
        if e.code == 404:
            raise ValueError(f'Not found: {url}')
        else:
            raise e


if __name__ == '__main__':
    main()
