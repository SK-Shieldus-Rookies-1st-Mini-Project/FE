
import streamlit as st
from malicious_news import crawl_malicious_news

def main():
    st.set_page_config(page_title="악성 웹사이트 뉴스", layout="wide")
    st.sidebar.title("지키링 네비게이션")
    page = st.sidebar.selectbox("페이지를 선택하세요", ["메인", "악성 웹사이트 뉴스"])

    if page == "메인":
        st.title("지키링 메인 페이지")
        st.write("원하는 기능을 네비게이션에서 선택하세요.")
    elif page == "악성 웹사이트 뉴스":
        st.title("악성 웹사이트 관련 최신 뉴스")
        st.write("실시간으로 악성 웹사이트 관련 뉴스를 크롤링하여 제공합니다.")
        with st.spinner('뉴스를 불러오는 중입니다...'):
            news = crawl_malicious_news()
        if news:
            for n in news:
                with st.container():
                    cols = st.columns([1, 4])
                    with cols[0]:
                        if n['img']:
                            st.image(n['img'], width=80)
                    with cols[1]:
                        st.markdown(f"**{n['title']}**")
                        with st.expander("본문 보기"):
                            # 상세 페이지에서 본문 크롤링
                            import requests
                            from bs4 import BeautifulSoup
                            try:
                                detail = requests.get(n['link'])
                                detail_soup = BeautifulSoup(detail.text, 'html.parser')
                                # 모바일 보안뉴스 본문 추출 (예시: .news_txt, 실제 구조에 따라 조정 필요)
                                content = detail_soup.select_one('.news_txt')
                                if content:
                                    st.write(content.get_text(strip=True))
                                else:
                                    st.write('본문을 불러올 수 없습니다.')
                            except Exception as e:
                                st.write('본문을 불러올 수 없습니다.')
        else:
            st.info("뉴스를 불러오지 못했습니다.")

if __name__ == "__main__":
    main()
