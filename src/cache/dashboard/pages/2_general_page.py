# --------------- Imports ---------------

from main import Cache
from ..dashboard import load_from_pickle

import streamlit as st

# --------------- General Information ---------------

st.set_page_config(
    page_title="General Information",
    page_icon="ℹ️"
)

st.title("General Cache Information ℹ️")
st.divider()

# Access stored cache in Session State
try:
    if "macho_cache" not in st.session_state:
        st.session_state.macho_cache = load_from_pickle()

    cache = st.session_state.macho_cache
except Exception as e:
    st.error(f"Failed ot load cache {e}")
    st.stop()


if cache is None:
    st.error("No caching metrics found in session state")
elif not isinstance(cache, Cache):
    st.error("The object currently in Session State is not a valid Cache-class object")
else:
    st.subheader("Configuration")
    st.json({
        "Max Cache Size": cache.max_cache_size,
        "Current Cache Size": cache.current_size,
        "Time-to-live": cache.ttl,
        "Eviction Strategy": cache.strategy,
        "Shard Count": cache.shard_count,
        "Bloom Filter Enabled": cache.bloom,
        "False Positive Rate": cache.probability if cache.bloom else "N/A"
    })
