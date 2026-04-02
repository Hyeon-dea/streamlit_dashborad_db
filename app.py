import streamlit as st
from db.init_db import create_table_customer, seed_customer_data
from db.connection import test_connection
from utils.state import init_session_state

st.set_page_config(
    page_title="Streamlit MySQL Dashboard",
    page_icon="📊",
    layout="wide"
    )

st.title("l Streamlit + MySQL 대시보드")
st.write("멀티페이지 기반 CRUD 및 시각화 대시보드 예제")

st.info("""
왼쪽 사이드바에서 페이지를 선택하세요.

1. 데이터조회
2. 판매관리
3. 고객관리
4. 시각화
5. 대시보드
""")

try: 
    result = test_connection()
    st.success(f'DB 연결 성공 (테스트 결과: {result})')
except Exception as e : 
    st.error(f'DB 연결 실패 : {e}')

init_session_state() # session state의 값들 초기화
#test_connection()
create_table_customer()  # DB가 생성되면 30, 31 줄을 주석처리
seed_customer_data()
