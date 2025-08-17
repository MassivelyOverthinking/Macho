# --------------- Imports ---------------

from main import Cache

import streamlit as st

# --------------- Metrics Dashboard ---------------

def rund_dashboard(cache: Cache) -> None:
    if "macho_cache" not in st.session_state:
        st.session_state.macho_cache = cache
    