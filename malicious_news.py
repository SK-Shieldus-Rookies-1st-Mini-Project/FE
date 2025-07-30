import requests
from bs4 import BeautifulSoup

def crawl_malicious_news():
    """
    악성 웹사이트 관련 뉴스를 크롤링하여 리스트로 반환합니다.
    각 뉴스는 {'title': 제목, 'img': 이미지URL, 'link': 링크} 형태의 딕셔너리입니다.
    """

    base_url = "https://m.boannews.com/html/"
    url = base_url + "Main_Menu.html?mkind=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news_list = []
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
        # 두 번째 span이 제목
        title = title_span[1].get_text(strip=True) if len(title_span) > 1 else ''
        news_list.append({'title': title, 'img': img_url, 'link': link})
    return news_list
