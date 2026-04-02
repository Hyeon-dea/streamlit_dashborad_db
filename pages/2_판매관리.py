import streamlit as st
from db.crud import (
    insert_sale, update_sale, delete_sale,
    get_sale_by_id, get_all_sales
)

st.title("🛠️ 판매 CRUD 관리")

tab1, tab2, tab3, tab4 = st.tabs(["조회", "등록", "수정", "삭제"])

with tab1:
    st.subheader("데이터 조회")
    df = get_all_sales()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("총 건수", len(df))

    with col2:
        total_qty = int(df["quantity"].sum()) if not df.empty else 0
        st.metric("총 수량", total_qty)

    with col3:
        total_amount = float((df["quantity"] * df["price"]).sum()) if not df.empty else 0
        st.metric("총 매출", f"{total_amount:,.0f} 원")

with tab2:
    st.subheader("데이터 등록")
    with st.form("insert_form"):
        order_date = st.date_input("주문일자")
        product_name = st.text_input("상품명")
        category = st.text_input("카테고리")
        quantity = st.number_input("수량", min_value=1, step=1)
        price = st.number_input("가격", min_value=0.0, step=1000.0)
        region = st.text_input("지역")
        submitted = st.form_submit_button("등록")

        if submitted:
            try:
                insert_sale(order_date, product_name, category, quantity, price, region)
                st.success("등록 완료")
            except Exception as e:
                st.error(f"등록 실패: {e}")

with tab3:
    st.subheader("데이터 수정")
    sale_id = st.number_input("수정할 ID", min_value=1, step=1, key="update_id")

    if st.button("불러오기"):
        row = get_sale_by_id(sale_id)
        if row:
            st.session_state["edit_row"] = row
        else:
            st.warning("해당 ID 데이터가 없습니다.")

    if "edit_row" in st.session_state:
        row = st.session_state["edit_row"]
        with st.form("update_form"):
            order_date = st.date_input("주문일자", value=row["order_date"])
            product_name = st.text_input("상품명", value=row["product_name"])
            category = st.text_input("카테고리", value=row["category"])
            quantity = st.number_input("수량", min_value=1, value=row["quantity"], step=1)
            price = st.number_input("가격", min_value=0.0, value=float(row["price"]), step=1000.0)
            region = st.text_input("지역", value=row["region"])
            updated = st.form_submit_button("수정 저장")

            if updated:
                try:
                    update_sale(sale_id, order_date, product_name, category, quantity, price, region)
                    st.success("수정 완료")
                    del st.session_state["edit_row"]
                except Exception as e:
                    st.error(f"수정 실패: {e}")

with tab4:
    st.subheader("데이터 삭제")
    delete_id = st.number_input("삭제할 ID", min_value=1, step=1, key="delete_id")
    if st.button("삭제 실행"):
        try:
            delete_sale(delete_id)
            st.success("삭제 완료")
        except Exception as e:
            st.error(f"삭제 실패: {e}")

st.divider()
st.subheader("현재 전체 데이터")
st.dataframe(get_all_sales(), use_container_width=True)