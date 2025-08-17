# --------------- Imports ---------------

from main import Cache

import streamlit as st

# --------------- General Information ---------------

st.set_page_config(
    page_title="General Information",
    page_icon="ℹ️"
)

st.title("General Cache Information ℹ️")
st.divider()

# Access stored cache in Session State
cache = st.session_state.get("macho_cache")

if cache is None:
    st.error("No caching metrics found in session state")
elif not isinstance(cache, Cache):
    st.error("The object currently in Session State is not a valid Cache-class object")
else:
    st.subheader("Configuration")
    st.json({
        "Max Cache Size": cache.max_cache_size,
        "Time-to-live": cache.ttl,
        "Eviction Strategy": cache.strategy,
        "Shard Count": cache.shard_count,
        "Bloom Filter Enabled": cache.bloom,
        "False Positive Rate": cache.probability if cache.bloom else "N/A"
    })
