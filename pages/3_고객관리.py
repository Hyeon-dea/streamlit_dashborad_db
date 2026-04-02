import streamlit as st
import pandas as pd
from db.crud import (get_filtered_customers,
                     insert_customer, 
                     update_customer, 
                     delete_customer)
from utils.pagination import paginate_df

st.title("🛠️ 고객관리 CRUD")

# 검색 폼
st.subheader('검색 조건')
with st.form('search customer'): 
    col1, col2, col3 = st.columns(3) 

    with col1: 
        name_keyword = st.text_input('이름', value=st.session_state.search_name)
    with col2:
        region = st.selectbox(
            "지역 선택",
            ["전체", "서울", "부산", "대구", "인천", "광주", "대전"],
            index=["전체", "서울", "부산", 
                   "대구", "인천", "광주", "대전"].index(st.session_state.search_region)
        )

    with col3:
        page_size = st.selectbox("페이지 크기", [5, 10, 20, 50], index=[5, 10, 20, 50].index(st.session_state.page_size))
    
    submitted = st.form_submit_button('검색')

    if submitted: 
        st.session_state.search_name = name_keyword 
        st.session_state.search_region = region
        st.session_state.page_size = page_size
        st.session_state.page_number = 1
    
df = get_filtered_customers(st.session_state.search_name, 
                            st.session_state.search_region)

page_df, total_pages = paginate_df(
    df,
    st.session_state.page_number,
    st.session_state.page_size
)

st.write(f"검색 결과: {len(df):,}건")

st.dataframe(page_df, use_container_width=True)

nav1, nav2, nav3 = st.columns([1, 2, 1])
with nav1:
    if st.button("이전"):
        if st.session_state.page_number > 1:
            st.session_state.page_number -= 1

with nav2:
    st.write(f"페이지 {st.session_state.page_number} / {total_pages}")

with nav3:
    if st.button("다음"):
        if st.session_state.page_number < total_pages:
            st.session_state.page_number += 1

st.divider()

# 신규고객 정보 등록
st.subheader("신규 고객 등록")

with st.form("insert_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("이름")
    with col2:
        region = st.selectbox("지역", ["서울", "부산", "대구", "인천", "광주", "대전"])
    with col3:
        age = st.number_input("나이", min_value=1, max_value=120, value=30)

    col4, col5 = st.columns(2)
    with col4:
        join_date = st.date_input("가입일")
    with col5:
        sales = st.number_input("매출액", min_value=0.0, value=100000.0, step=1000.0)

    submitted_insert = st.form_submit_button("등록")

    if submitted_insert:
        insert_customer(name, region, age, join_date, sales)
        st.success("고객이 등록되었습니다.")

st.divider()

# 고객 정보 갱신/삭제
st.subheader("수정 / 삭제")

if not df.empty:
    selected_id = st.selectbox("수정/삭제할 고객 ID 선택", df["id"].tolist())
    selected_row = df[df["id"] == selected_id].iloc[0]

    with st.form("update_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            u_name = st.text_input("이름", value=selected_row["name"])
        with col2:
            u_region = st.selectbox(
                "지역",
                ["서울", "부산", "대구", "인천", "광주", "대전"],
                index=["서울", "부산", "대구", "인천", "광주", "대전"].index(selected_row["region"])
            )
        with col3:
            u_age = st.number_input("나이", min_value=1, max_value=120, value=int(selected_row["age"]))

        col4, col5 = st.columns(2)
        with col4:
            u_join_date = st.date_input("가입일", value=pd.to_datetime(selected_row["join_date"]).date())
        with col5:
            u_sales = st.number_input("매출액", min_value=0.0, value=float(selected_row["sales"]), step=1000.0)

        c1, c2 = st.columns(2)
        with c1:
            submitted_update = st.form_submit_button("수정")
        with c2:
            submitted_delete = st.form_submit_button("삭제")

        if submitted_update:
            update_customer(selected_id, u_name, u_region, u_age, u_join_date, u_sales)
            st.success("수정이 완료되었습니다.")

        if submitted_delete:
            delete_customer(selected_id)
            st.warning("삭제가 완료되었습니다.")
else:
    st.info("수정/삭제할 데이터가 없습니다.")