import streamlit as st

def init_session_state():
    defaults = {
        "search_name": "",
        "search_region": "전체",
        "page_number": 1,
        "page_size": 10,
        "selected_customer_id": None,
        "dashboard_refresh_count": 0,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value