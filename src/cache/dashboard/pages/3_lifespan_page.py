# --------------- Imports ---------------

from src.cache.main import Cache
from src.cache.dashboard import load_from_pickle

from src.cache.errors import MetricsLifespanException

import streamlit as st
import pandas as pd
import plotly.express as px

# --------------- Lifespan Metrics ---------------

st.title("Entry Lifespan Data ⌛")
st.divider()
st.subheader("Metrics & Data visualisation regarding individual and overall lifespan of caching entries.")

# Access stored cache in Session State
try:
    if "macho_cache" not in st.session_state:
        st.session_state.macho_cache = load_from_pickle()

    cache = st.session_state.macho_cache
except Exception as e:
    st.error(f"Failed ot load cache {e}")
    st.stop()

# Manage Streamlit tabs
tabs = st.tabs(["📊 Summary", "📉 Histogram", "📦 Box Plot"])

if cache is None:
    st.error("No metrics found in current session state")
elif not isinstance(cache, Cache):
    st.error("The object currently in Session State is not a valid Cache-object")
else:
    if isinstance(cache.cache, list): # Shared Cache

        try:
            lifespan_data = [ch.metric_lifespan for ch in cache.cache]
            all_lifespan = [
                {"Shard": i, "Lifespan": val}
                for i, entry in enumerate(cache.cache)
                for val in entry.lifespan
            ]
        except MetricsLifespanException as e:
            st.error(f"No lifespan data currently available {e}")
        else:
            shard_df = pd.DataFrame([
                {
                    "Shard": index,
                    "Max": data["max"],
                    "Min": data["min"],
                    "Count": data["count"],
                    "Total": data["total"],
                    "Average": data["average"],
                    "Median": data["median"]
                }
                for index, data in enumerate(lifespan_data)
            ])

            with tabs[0]:
                st.subheader("Summary of Lifespan Metrics")
                st.dataframe(shard_df)
                st.plotly_chart(px.bar(
                    shard_df.melt(id_vars="Shard", var_name="Metric", value_name="Value"),
                    x="Shard",
                    y="Value",
                    color="Metric",
                    barmode="group",
                    title="Lifespan Metrics pr. Shard"
                ))

                with st.expander("View Raw Summary Table"):
                    st.dataframe(shard_df)

            with tabs[1]:
                st.subheader("Distribution of Lifespan Metrics")
                lfsp_data = pd.DataFrame(all_lifespan)
                st.dataframe(lfsp_data)
                bins = st.slider("Number of bins", min_value=10, max_value=100, value=30)
                st.plotly_chart(px.histogram(
                    lfsp_data,
                    x="Lifespan",
                    color="Shard",
                    nbins=bins,
                    barmode="overlay",
                    opacity=0.6,
                    title="Entry Lifespan Distribution pr. shard"
                ))

                if st.checkbox("Show Raw Lifespan Data"):
                    st.dataframe(lfsp_data)

            with tabs[2]:
                st.subheader("Box Plot pr. Shard")
                st.plotly_chart(px.box(
                    lfsp_data,
                    x="Shard",
                    y="Lifespan",
                    points="outliers",
                    title="Lifespan Spread pr. Shard"
                ))
    
    else: # Individual Cache
        st.subheader("Single Cache Lifespan Metrics")

        try:
            lifespan_data = cache.cache.metric_lifespan
            entry_lifespans = cache.cache.lifespan
        except MetricsLifespanException as e:
            st.error(f"No lifespan data currently available {e}")
        else:
            lifespan_df = pd.DataFrame([
                {"Metric": k.capitalize(), "Value": v}
                for k, v in lifespan_data.items()
            ])

            with tabs[0]:
                st.subheader("Summary of Lifespan Metrics")
                st.dataframe(lifespan_df)
                st.plotly_chart(px.bar(
                    lifespan_df,
                    x="Metric",
                    y="Value",
                    title="Lifespan Metrics"
                ))

                with st.expander("View Raw Summary Data"):
                    st.dataframe(lifespan_df)

            with tabs[1]:
                st.subheader("Distribution of Entry Lifespans")
                new_df = pd.DataFrame(entry_lifespans, columns=["Lifespan"])
                bins = st.slider("Number of bins", min_value=10, max_value=100, value=30)
                if entry_lifespans:
                    st.plotly_chart(px.histogram(
                        new_df,
                        x="Lifespan",
                        nbins=bins,
                        title="Entry Lifespan Distribution",
                        labels={"Value": "Lifespan(s)"},
                        opacity=0.7
                    ))

                    if st.checkbox("Show Raw Lifespan Data"):
                        st.dataframe(new_df)

            with tabs[2]:
                st.subheader("Box Plot of Lifespans")
                if entry_lifespans:
                    df = pd.DataFrame({"Lifespan": entry_lifespans})
                    st.plotly_chart(px.box(
                        df, 
                        y="Lifespan",
                        points="outliers",
                        title="Lifespan Spread"
                    ))
