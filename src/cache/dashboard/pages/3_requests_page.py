# --------------- Imports ---------------

from main import Cache

import streamlit as st

# --------------- Requests Metrics ---------------

st.set_page_config(
    page_title="Requests Metrics",
    page_icon="📚"
)

st.title("Cache Requests Data 📚")
st.divider()
st.subheader("Metrics & Data visualisation regarding total requests made towards the Cache.")

# Access stored cache in Session State
cache = st.session_state.get("macho_cache")