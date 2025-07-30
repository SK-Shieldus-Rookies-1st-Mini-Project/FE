import streamlit as st
from malicious_news import crawl_malicious_news

def main():
    st.set_page_config(page_title="온라인 보안 뉴스", layout="wide")
    st.sidebar.title("지키링 네비게이션")
    page = st.sidebar.selectbox("페이지를 선택하세요", ["메인", "온라인 보안 뉴스"])

    if page == "메인":
        st.title("지키링")
        st.write("원하는 기능을 네비게이션에서 선택하세요.")
        # 가운데 정렬 및 여백을 위한 columns 사용
        left, center, right = st.columns([2, 4, 2])
        with center:
            user_url = st.text_input("악성 여부를 확인할 URL을 입력하세요", "")
            if user_url:
                st.info(f"입력한 URL: {user_url}")
    elif page == "온라인 보안 뉴스":
        st.title("온라인 보안 관련 최신 뉴스")
        st.write("실시간으로 온라인 보안 관련 뉴스를 크롤링하여 제공합니다.")
        search_query = st.text_input("뉴스 제목 검색", "")
        with st.spinner('뉴스를 불러오는 중입니다...'):
            news = crawl_malicious_news()
        if news:
            filtered_news = [n for n in news if search_query.strip() == "" or search_query.lower() in n['title'].lower()]
            if not filtered_news:
                st.info("검색어를 포함하는 뉴스가 없습니다.")
            for n in filtered_news:
                with st.container():
                    cols = st.columns([1, 4])
                    with cols[0]:
                        if n['img']:
                            st.image(n['img'], width=80)
                    with cols[1]:
                        st.markdown(f"**{n['title']}**")
                        with st.expander("본문 보기"):
                            import requests
                            from bs4 import BeautifulSoup
                            try:
                                detail = requests.get(n['link'])
                                detail_soup = BeautifulSoup(detail.text, 'html.parser')
                                content = detail_soup.select_one('.con #con')
                                if content:
                                    html = str(content)
                                    st.markdown(f"<div style='margin-bottom:10px; line-height:1.7; font-size:10px !important;'>{html}</div>", unsafe_allow_html=True)
                                else:
                                    og_desc = detail_soup.find('meta', attrs={'property': 'og:description'})
                                    if og_desc and og_desc.get('content'):
                                        st.markdown(f"<div style='margin-bottom:10px; line-height:1.7; font-size:10px !important;'>{og_desc['content']}</div>", unsafe_allow_html=True)
                                    else:
                                        st.write('본문을 불러올 수 없습니다.')
                            except Exception as e:
                                st.write('본문을 불러올 수 없습니다.')
        else:
            st.info("뉴스를 불러오지 못했습니다.")

if __name__ == "__main__":
    main()