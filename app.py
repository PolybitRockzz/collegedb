import streamlit as st
import os
import json
from datetime import datetime

# Check for settings.json and create with defaults if missing
settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
if not os.path.exists(settings_path):
    default_settings = {
        "last_ran_parser": "never",
        "ollama_model": "qwen2.5vl:7b"
    }
    with open(settings_path, "w") as f:
        json.dump(default_settings, f, indent=4)

database_page = st.Page("database.py", title="Database", icon=":material/database:")
parser_page = st.Page("parser.py", title="Parser", icon=":material/terminal:")
pg = st.navigation([database_page, parser_page])
pg.run()