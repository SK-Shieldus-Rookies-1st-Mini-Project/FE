import requests
from bs4 import BeautifulSoup

def crawl_malicious_news(max_page=3):
    """
    보안뉴스 모바일 '더보기' AJAX를 활용해 여러 페이지의 뉴스를 크롤링합니다.
    max_page: 몇 페이지까지 가져올지(1=최신, 2=더보기 1번, ...)
    """
    base_url = "https://m.boannews.com/html/"
    ajax_url = base_url + "Main_Menu.html"
    news_list = []

    for page in range(1, max_page + 1):
        params = {"mkind": 1, "page1": page}
        response = requests.get(ajax_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        for li in soup.select('ul.tab-newslist li'):
            a_tag = li.find('a', href=True)
            if not a_tag:
                continue
            link = a_tag['href']
            if not link.startswith('http'):
                link = base_url + link
            img_tag = a_tag.find('img')
            img_url = img_tag['src'] if img_tag else ''
            title_span = a_tag.find_all('span')
            title = title_span[1].get_text(strip=True) if len(title_span) > 1 else ''
            news_list.append({'title': title, 'img': img_url, 'link': link})
    return news_list