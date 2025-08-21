# --------------- Imports ---------------

from src.cache.main import Cache
from src.cache.logging import get_logger

import streamlit.web.cli as stcli
import streamlit as st

import pickle
import sys
import os
import tempfile

# --------------- Logging setup ---------------

logger = get_logger(__name__)

# --------------- Pickle Path ---------------

PICKLE_PATH = os.environ.get(
    "MACHO_CACHE_PICKLE_PATH",
    os.path.join(tempfile.gettempdir(), "macho_cache.pkl")
)
print(PICKLE_PATH)

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

# --------------- Launch Metrics Dashboard ---------------
    
def load_from_pickle() -> Cache:
    if not os.path.exists(PICKLE_PATH):
        raise FileNotFoundError("No cache object found in persistent storage")
    
    with open(PICKLE_PATH, "rb") as f:
        cache = pickle.load(f)

    if not hasattr(cache, "cache"):
        raise AttributeError("Cache object missing attribute 'cache' after unpickling")
    
    if isinstance(cache, list):
        for index, shard in enumerate(cache):
            if not hasattr(shard, "cache"):
                raise AttributeError(f"Cache shard {index} is missing 'cache' attribute")
    
    return cache


def run_dashboard(cache: Cache) -> None:

    with open(PICKLE_PATH, "wb") as f:
        pickle.dump(cache, f)

    # Runs the Streamlit server from a subprocess
    script_path = os.path.abspath(__file__)
    dsh_dir = os.path.dirname(script_path)
    final_path = os.path.join(dsh_dir, "dashboard.py")

    logger.debug(f"Launching Streamlit dashboard from path {final_path}")

    sys.argv = ["streamlit", "run", final_path]
    sys.exit(stcli.main())
    