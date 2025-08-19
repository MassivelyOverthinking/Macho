# --------------- Imports ---------------

from main import Cache
from itertools import zip_longest

from ...errors import MetricsLatencyException

import streamlit as st
import pandas as pd
import plotly.express as px

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

# Manage Streamlit Tabs
tabs = st.tabs(["📉 Line Charts", "📊 Histograms", "📦 Box Plots"])

if cache is None:
    st.error("No metrics found in current session state")
elif not isinstance(cache, Cache):
    st.error("The object currently in Session State is not a valid Cache-object")
else:
    if isinstance(cache.cache, list): # shared cache

        try:
            shared_latency_data = [ch.latencies for ch in cache.cache]
            all_shared_latencies = [
                {"Shard": index, "Type": "Get", "Latency": get_l}
                for index, entry in enumerate(cache.cache)
                for get_l in entry.get_latency
            ] + [
                {"Shard": index, "Type": "Add", "Latency": add_l}
                for index, entry in enumerate(cache.cache)
                for add_l in entry.add_latency
            ]
        except MetricsLatencyException as e:
            st.error("No Latency Data currently available")
        else:
            shard_latency_df = pd.DataFrame([
                {
                    "Shard": index,
                    "Avg. Add Latency": data["add_latency_seconds"],
                    "Max Add Latency": data["max_add_latency"],
                    "Min Add Latency": data["min_latency_data"],
                    "Avg. Get Latency": data["get_latency_seconds"],
                    "Max Get Latency": data["max_get_latency"],
                    "Min Get Latency": data["min_get_latency"]
                }
                for index, data in enumerate(shared_latency_data)
            ])

            with tabs[0]:
                st.subheader("Line Charts for Cache Latency")
                st.dataframe(shard_latency_df)
                st.plotly_chart(px.line(
                    shard_latency_df.melt(id_vars="Shard", var_name="Metric", value_name="Latency(s)"),
                    x="Shard",
                    y="Value",
                    color="Metric",
                    markers=True,
                    title="Latency Metrics per Shard",
                    template="plotly"
                ))

                with st.expander("View Raw Summary Data"):
                    st.dataframe(shard_latency_df)

            with tabs[1]:
                st.subheader("Histograms for Cache Latencies")
                hist_latency_data = pd.DataFrame(all_shared_latencies)
                st.dataframe(hist_latency_data)

                shared_bins = st.slider(min_value=10, max_value=100, value=30)

                st.plotly_chart(px.histogram(
                    hist_latency_data,
                    x="Latency",
                    color="Type",
                    nbins=shared_bins,
                    barmode="overlay",
                    opacity=0.6,
                    title="Method Latency Distribution per Shard"
                ))

                if st.checkbox("Show Raw Latency Data"):
                    st.dataframe(all_shared_latencies)

            with tabs[2]:
                st.subheader("Box Plot per shard")
                st.plotly_chart(px.box(
                    all_shared_latencies,
                    x="Shard",
                    y="Latency",
                    points="outliers",
                    title="Latency Spread per Shard"
                ))
    else: # Single Cache
        st.subheader("Single Cache Latency Metrics")

        try:
            single_latency_data = cache.cache.latencies
            all_single_latencies = cache.cache.get_latency + cache.cache.add_latency
        except MetricsLatencyException as e:
            st.error(f"No latency data currently available {e}")
        else:
            latency_df = pd.DataFrame([
                {"Metric": key.capitalize(), "Value": value}
                for key, value in single_latency_data.items() 
            ])

            with tabs[0]:
                st.subheader("Line Charts for Cache Latency")
                st.dataframe(latency_df)
                st.plotly_chart(px.line(
                    latency_df,
                    x="Metric",
                    y="Value",
                    title="Latency Metrics"
                ))

                with st.expander("View Raw Latency Data"):
                    st.dataframe(latency_df)

            with tabs[1]:
                st.subheader("Histograms for Cache Latencies")
                all_entry_latency_data = pd.DataFrame(all_single_latencies, columns=["Latency"])

                single_bins = st.slider(min_value=10, max_value=100, value=30)

                if all_single_latencies:
                    st.plotly_chart(px.histogram(
                        all_entry_latency_data,
                        x="Latency",
                        nbins=single_bins,
                        title="Entry Latency Distribution",
                        labels={"Value": "Latency(s)"},
                        opacity=0.7
                    ))

                    if st.checkbox("Show Raw Latency Data"):
                        st.dataframe(all_entry_latency_data)

            with tabs[2]:
                st.subheader("Box Plot for Single Cache")
                if all_single_latencies:
                    df = pd.DataFrame({"Latency": all_single_latencies})
                    st.plotly_chart(px.box(
                        df,
                        y="Latency",
                        points="outliers",
                        title="Latency Spread"
                    ))