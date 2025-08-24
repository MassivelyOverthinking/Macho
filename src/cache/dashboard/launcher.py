# --------------- Imports ---------------

from ..logging.logger_config import get_logger
from ..main import Cache

from typing import Dict, Any

import streamlit.web.cli as stcli

import json
import os
import tempfile
import sys


# --------------- Logging setup ---------------

logger = get_logger(__name__)       # Get logger equipped with Rotating File Handler.

# --------------- JSON Data Path ---------------

JSON_DATA_PATH = os.environ.get(
    "MACHO_CACHE_JSON_PATH",
    os.path.join(tempfile.gettempdir(), "macho_cache.json")
)
print(JSON_DATA_PATH)

# --------------- Streamlit Dashboard Launcher ---------------

def load_from_json() -> Dict[str, Any]:       # Loads data for Streamlit dashboard from persistent storage
    if not os.path.exists(JSON_DATA_PATH):
        raise FileNotFoundError(f"No data found in persistent storage")
    
    with open(JSON_DATA_PATH, "rb") as tmp: 
        metrics_data = json.load(tmp)   # Retreives data

    return metrics_data     # Returns data in a dictionary formats



def launch_dashboard(cache: Cache) -> None:
    if not isinstance(cache, Cache):
        raise TypeError(f"Paramter 'cache' must be of Type: Cache, not {type(cache)}")
    
    macho_cache_metrics = cache.get_metrics()
    
    with open(JSON_DATA_PATH, "wb") as f:   # Immediately allocates data to persistent storage.
        json.dump(macho_cache_metrics, f)

    # Runs the Streamlit server from a subprocess
    script_path = os.path.abspath(__file__)
    dsh_dir = os.path.dirname(script_path)
    final_path = os.path.join(dsh_dir, "dashboard.py")

    logger.debug(f"Launching Streamlit dashboard from path {final_path}")

    sys.argv = ["streamlit", "run", final_path]
    sys.exit(stcli.main())