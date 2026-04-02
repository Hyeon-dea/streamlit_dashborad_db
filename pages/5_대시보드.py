# 고객 테이블 데이터의 요약/주요 정보 대시보드화 구성
import streamlit as st
import plotly.express as px

from db.crud import get_summary, get_region_summary, get_all_customers


st.title("📌 대시보드")

summary_df = get_summary()
row = summary_df.iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("총 고객수", f"{int(row['customer_count']):,}")
c2.metric("평균 나이", f"{row['avg_age']}")
c3.metric("총 매출", f"{row['total_sales']:,.0f}")
c4.metric("평균 매출", f"{row['avg_sales']:,.0f}")

st.subheader("지역별 고객 및 매출 현황")
region_df = get_region_summary()

col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(region_df, x="region", y="customer_count", title="지역별 고객수")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(region_df, names="region", values="total_sales", title="지역별 매출 비중")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("최근 등록 고객")
recent_df = get_all_customers().head(10)
st.dataframe(recent_df, use_container_width=True)

@st.fragment
def refresh_panel():
    st.subheader("🔄 부분 갱신 패널")
    if st.button("새로고침 횟수 증가"):
        st.session_state.dashboard_refresh_count += 1
    st.write("현재 fragment 새로고침 횟수:", st.session_state.dashboard_refresh_count)

refresh_panel()