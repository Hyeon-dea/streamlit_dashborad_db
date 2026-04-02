import streamlit as st
from sqlalchemy import create_engine, text

# Local에 있는 MySQL DB 연결
# # DB 연결
# @st.cache_resource
# def get_engine():
#     db = st.secrets["mysql"]
#     url = (
#         f"mysql+pymysql://{db['user']}:{db['password']}"
#         f"@{db['host']}:{db['port']}/{db['database']}"
#         f"?charset={db['charset']}"
#     )
#     engine = create_engine(url, pool_pre_ping=True)
#     return engine

# AWS RDS의 MySQL 연결
@st.cache_resource
def get_engine():
    engine = st.connection('dashboard_db', type='sql').engine
    return engine

# DB 연결 테스트
def test_connection():
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        return result.scalar()