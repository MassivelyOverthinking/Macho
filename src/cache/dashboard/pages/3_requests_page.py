# --------------- Imports ---------------

from main import Cache
from ..dashboard import load_from_pickle

import streamlit as st
import pandas as pd
import plotly.express as px

# --------------- Requests Metrics ---------------

st.set_page_config(
    page_title="Requests Metrics",
    page_icon="📚"
)

st.title("Cache Requests Data 📚")
st.divider()
st.subheader("Metrics & Data visualisation regarding total requests made towards the Cache.")

# Access stored cache in Session State
try:
    if "macho_cache" not in st.session_state:
        st.session_state.macho_cache = load_from_pickle()

    cache = st.session_state.macho_cache
except Exception as e:
    st.error(f"Failed ot load cache {e}")
    st.stop()

if cache is None:
    st.error("No metrics found in current session state")
elif not isinstance(cache, Cache):
    st.error("The obejct currently in Session State is not a valid Cache-object")
else:
    if isinstance(cache.cache, list):
        st.subheader("Shared Cache Metrics")

        shard_df = pd.DataFrame([
            {
                "Shard": index,
                "Hit Ratio": shard.hit_ratio,
                "Hits": shard.hits,
                "Misses": shard.misses,
                "Evictions": shard.evictions
            }
            for index, shard in enumerate(cache.cache)
        ])

        st.plotly_chart(px.bar(
            shard_df,
            x="Shard",
            y=["Hits", "Misses", "Evictions"],
            barmode="group",
            title="Cache activity pr. Cahcing System"
        ))

        st.plotly_chart(px.line(
            shard_df,
            x="Shard",
            y="Hit Ratio",
            title="Hit ratio pr. second"
        ))

    else:
        st.subheader("Single Cache Metrics")

        single_data = cache.cache.metrics

        single_df = pd.DataFrame([{
            "Hits": single_data["hits"],
            "Misses": single_data["misses"],
            "Evictions": single_data["evictions"],
            "Hit Ratio": single_data["hit_ratio"]
        }])

        st.plotly_chart(px.bar(
            single_df.melt(var_name="Metric", value_name="Value"),
            x="Metric",
            y="Value",
            title="Single Cachen Operations"
        ))








