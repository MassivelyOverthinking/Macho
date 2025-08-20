# --------------- Imports ---------------

from ..main import Cache

import streamlit as st
import streamlit.web.cli as stcli

import pickle

import sys
import os


# --------------- Metrics Dashboard ---------------

PICKLE_PATH = "/tmp/macho_cache.pkl"
    
def load_from_pickle() -> Cache:
    if not os.path.exists(PICKLE_PATH):
        raise FileNotFoundError("No cache object found in persistent storage")
    
    with open(PICKLE_PATH, "rb") as f:
        return pickle.load()


def run_dashboard(cache: Cache) -> None:

    with open(PICKLE_PATH, "wb") as f:
        pickle.dump(cache, f)

    # Runs the Streamlit server from a subprocess
    script_path = os.path.abspath(__file__)
    dsh_dir = os.path.dirname(script_path)
    final_path = os.path.join(dsh_dir, "1_main_page.py")
    sys.argv = ["streamlit", "run", final_path]
    sys.exit(stcli.main())
    