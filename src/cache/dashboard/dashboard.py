# --------------- Imports ---------------

from main import Cache

import streamlit as st
import streamlit.web.cli as stcli

import sys
import os


# --------------- Metrics Dashboard ---------------

def run_dashboard(cache: Cache) -> None:

    # Add the cache instance to Session State if not already present.
    if "macho_cache" not in st.session_state:
        st.session_state.macho_cache = cache

    # Runs the Streamlit server from a subprocess
    script_path = os.path.abspath(__file__)
    dsh_dir = os.path.dirname(script_path)
    final_path = os.path.join(dsh_dir, "dashboard.py")
    sys.argv = ["streamlit", "run", final_path]
    sys.exit(stcli.main())
    