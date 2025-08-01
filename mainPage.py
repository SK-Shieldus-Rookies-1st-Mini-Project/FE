import streamlit as st
import pymysql
import pandas as pd
from malicious_news import crawl_malicious_news

# DB에서 특정 URL의 악성 여부 조회 함수
def get_url_result(url):
    try:
        conn = pymysql.connect(
            host='localhost',
            user='python',
            password='python',
            db='python_db',
            charset='utf8mb4'
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT result FROM test WHERE url = %s", (url,))
            row = cursor.fetchone()
            return row[0] if row else None
    except Exception as e:
        st.error(f"❌ DB 조회 오류: {e}")
        return None
    finally:
        conn.close()

# DB 전체 기록 로드 함수 (표시용)
def load_from_DB():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='python',
            password='python',
            db='python_db',
            charset='utf8mb4'
        )
        query = "SELECT url, url_len, url_entropy, result FROM test"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"❌ 전체 데이터 로딩 오류: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# 메인 실행 함수
def main():
    st.set_page_config(page_title="온라인 보안 뉴스", layout="wide")
    st.sidebar.title("지키링 네비게이션")
    page = st.sidebar.selectbox("페이지를 선택하세요", ["메인", "온라인 보안 뉴스"])

    if page == "메인":
        st.title("지키링")
        st.write("원하는 기능을 네비게이션에서 선택하세요.")

        # 가운데 입력창
        left, center, right = st.columns([2, 4, 2])
        with center:
            user_url = st.text_input("🔎 악성 여부를 확인할 URL을 입력하세요", "")
            if user_url:
                st.info(f"입력한 URL: {user_url}")
                result = get_url_result(user_url)

                if result is None:
                    st.warning("🤔 이 URL은 아직 분석되지 않았습니다.")
                elif result == 1:
                    st.success(f"✅ {user_url} 사이트는 **정상 사이트입니다.**")
                elif result == -1:
                    st.error(f"🚨 {user_url} 사이트는 **악성 사이트입니다.**")
                else:
                    st.info(f"⚠️ 분류되지 않은 결과값: {result}")

        # 판별 이력 테이블
        st.subheader("📊 URL 판별 이력")
        df_history = load_from_DB()
        if not df_history.empty:
            df_history['result'] = df_history['result'].map({1: '정상', -1: '악성'}).fillna('미분류')
            st.dataframe(df_history)
        else:
            st.info("아직 저장된 URL 정보가 없습니다.")

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
                            except Exception:
                                st.write('본문을 불러올 수 없습니다.')
        else:
            st.info("뉴스를 불러오지 못했습니다.")

if __name__ == "__main__":
    main()
