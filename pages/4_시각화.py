import streamlit as st
import plotly.express as px
from db.crud import get_all_customers, get_all_sales
from utils.charts import (
    sales_by_category_chart,
    sales_by_region_chart,
    sales_trend_chart
)

st.title("📈 시각화")

df_sale = get_all_sales()
df_customers = get_all_customers()

tab1, tab2 = st.tabs(["매출 시각화", "고객 시각화"])

with tab1:
    if df_sale.empty:
        st.warning("시각화할 데이터가 없습니다.")
    else:
        st.plotly_chart(sales_by_category_chart(df_sale), use_container_width=True)
        st.plotly_chart(sales_by_region_chart(df_sale), use_container_width=True)
        st.plotly_chart(sales_trend_chart(df_sale), use_container_width=True)

with tab2:
    if df_customers.empty:
        st.info("표시할 데이터가 없습니다.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("나이 분포")
            fig1 = px.histogram(df_customers, x="age", nbins=10, title="고객 나이 분포")
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.subheader("지역별 평균 매출")
            avg_df = df_customers.groupby("region", as_index=False)["sales"].mean()
            fig2 = px.bar(avg_df, x="region", y="sales", title="지역별 평균 매출")
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("원본 데이터 요약")
        st.dataframe(df_customers.describe(include="all"), use_container_width=True)