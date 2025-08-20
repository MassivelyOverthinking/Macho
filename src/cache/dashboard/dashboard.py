# --------------- Imports ---------------

from src.cache.main import Cache

import streamlit.web.cli as stcli
import streamlit as st

import pickle
import sys
import os
import tempfile

# --------------- Metrics Dashboard ---------------

PICKLE_PATH = os.environ.get(
    "MACHO_CACHE_PICKLE_PATH",
    os.path.join(tempfile.gettempdir(), "macho_cache.pkl")
)

# --------------- Main Page ---------------

st.set_page_config(
    page_title="Macho Caching Metrics",
    page_icon="👋"
)

st.title("Welcome to Macho Metrics Dashboard! 👋")
st.divider()
st.markdown(
    """
    Macho's extensive metrics dashboard provides you with concrete data for optimizing, analyzing,
    and streamlining caching opreations.

    **👈 Select options from the navigation bar** to views metrics.

    ### For further information visit regarding Macho:
    - (Not yet implemented)
    """
)
    
def load_from_pickle() -> Cache:
    if not os.path.exists(PICKLE_PATH):
        raise FileNotFoundError("No cache object found in persistent storage")
    
    with open(PICKLE_PATH, "rb") as f:
        return pickle.load(f)


def run_dashboard(cache: Cache) -> None:

    with open(PICKLE_PATH, "wb") as f:
        pickle.dump(cache, f)

    # Runs the Streamlit server from a subprocess
    script_path = os.path.abspath(__file__)
    dsh_dir = os.path.dirname(script_path)
    final_path = os.path.join(dsh_dir, "dashboard.py")
    sys.argv = ["streamlit", "run", final_path]
    sys.exit(stcli.main())
    