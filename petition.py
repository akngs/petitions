import csv
import os
from typing import Dict
from urllib import request
from urllib.error import HTTPError

from bs4 import BeautifulSoup

CSV_FILE = 'petition.csv'


def main():
    latest_id = get_latest_article_id()
    next_id = get_latest_saved_article_id() + 1
    for i in range(next_id, latest_id):
        try:
            article = fetch_article(i)
            save_article(article)
        except ValueError:
            pass


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


def fetch_article(article_id: int) -> Dict[str, any]:
    """글번호에 해당하는 글의 HTML 텍스트를 가져와서 파싱. 해당 글이 없거나 형식이 다르면 ValueError"""
    url = f'https://www1.president.go.kr/petitions/{article_id}'
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html5lib")

    return {
        'article_id': article_id,
        'title': soup.select('.petitionsView_title', limit=1)[0].text,
        'votes': int(soup.select('.petitionsView_count .counter', limit=1)[0].text),
        'category': soup.select('.petitionsView_info_list li:nth-of-type(1)', limit=1)[0].text[4:],
        'start': soup.select('.petitionsView_info_list li:nth-of-type(2)', limit=1)[0].text[4:],
        'end': soup.select('.petitionsView_info_list li:nth-of-type(3)', limit=1)[0].text[4:],
        'content': soup.select('.View_write')[0].text,
    }


def save_article(article: Dict[str, any]) -> None:
    """글을 CSV 형태로 저장한다"""
    cols = ['article_id', 'start', 'end', 'votes', 'category', 'title', 'content']

    # 파일이 없으면 새로 만들고 칼럼 이름 저장
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(cols)

    # 새로운 행 추가
    with open(CSV_FILE, 'a', newline='') as f:
        w = csv.writer(f)
        w.writerow(article[col] for col in cols)


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
