# --------------- Imports ---------------

from main import Cache

import streamlit as st

# --------------- Lifespan Metrics ---------------

st.set_page_config(
    page_title="Lifespan Metrics",
    page_icon="⌛"
)

st.title("Entry Lifespan Data ⌛")
st.divider()
st.subheader("Metrics & Data visualisation regarding individual and overall lifespan of caching entries.")

# Access stored cache in Session State
cache = st.session_state.get("macho_cache")

if cache is None:
    st.error("No metrics found in current session state")
elif not isinstance(cache, Cache):
    st.error("The obejct currently in Session State is not a valid Cache-object")
else:
    st.subheader()