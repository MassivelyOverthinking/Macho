# --------------- Imports ---------------

from macho.dashboard import load_from_json

import streamlit as st

# --------------- General Information ---------------

st.title("General Cache Information ℹ️")
st.divider()

# Access stored cache data in Session State
try:
    if "macho_metrics" not in st.session_state:
        st.session_state["macho_metrics"] = load_from_json()    # Loads data from persistent storage.

    macho_cache_metrics = st.session_state["macho_metrics"]
except Exception as e:
    st.error(f"Failed to load cache data {e}")
    st.stop()


if macho_cache_metrics is None:
    st.error("No caching metrics found in session state")
elif not isinstance(macho_cache_metrics, (dict, list)):
    st.error("The object currently in Session State is not a valid Cache-class object")
else:
    st.subheader("Configuration")
    st.json({
        "Max Cache Size": macho_cache_metrics["max_cache_size"],
        "Current Cache Size": macho_cache_metrics["current_size"],
        "Time-to-live": macho_cache_metrics["ttl"],
        "Eviction Strategy": macho_cache_metrics["eviction_strategy"],
        "Shard Count": macho_cache_metrics["shard_count"],
        "Bloom Filter Enabled": macho_cache_metrics["bloom"],
        "False Positive Rate": macho_cache_metrics["probability"] if macho_cache_metrics["bloom"] else "N/A"
    })
