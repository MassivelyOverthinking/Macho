# --------------- Imports ---------------

from main import Cache

import streamlit as st

# --------------- Latency Metrics ---------------

st.set_page_config(
    page_title="Latency Metrics",
    page_icon="⏱️"
)

st.title("Function Latency Data ⏱️")
st.divider()
st.subheader("Metrics & Data visualisation of the time it takes to perform individual function calls.")

# Access stored cache in Session State
cache = st.session_state.get("macho_cache")