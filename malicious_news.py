import requests
from bs4 import BeautifulSoup

def crawl_malicious_news():
    """
    Main_Menu.html에서 모든 뉴스 목록을 가져오고,
    각 뉴스의 detail 페이지에서 제목/이미지/본문을 추출합니다.
    """
    base_url = "https://m.boannews.com/html/"
    url = base_url + "Main_Menu.html"
    params = {"page1": 1}
    news_list = []

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    for li in soup.select('ul.tab-newslist li'):
        a_tag = li.find('a', href=True)
        if not a_tag:
            continue
        href = a_tag['href']
        if not href.startswith('http'):
            detail_url = base_url + href
        else:
            detail_url = href
        try:
            detail_resp = requests.get(detail_url)
            detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')
            # 제목
            title_tag = detail_soup.select_one('div.tit > p')
            title = title_tag.get_text(strip=True) if title_tag else ''
            # 이미지
            img_tag = detail_soup.find('meta', attrs={'property': 'og:image'})
            img_url = img_tag['content'] if img_tag and img_tag.get('content') else ''
            # 본문
            content_tag = detail_soup.select_one('.con #con')
            content = str(content_tag) if content_tag else ''
        except Exception:
            title = ''
            img_url = ''
            content = ''
        if title:
            news_list.append({'title': title, 'img': img_url, 'link': detail_url, 'content': content})
    return news_list