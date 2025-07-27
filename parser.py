import streamlit as st
import os
import json
from datetime import datetime
import subprocess

def get_last_ran_parser():
    settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
    if not os.path.exists(settings_path):
        return "never"
    with open(settings_path, "r") as f:
        settings = json.load(f)
    return settings.get("last_ran_parser", "never")

def main():
    st.set_page_config(page_title="CollegeDB - Parser", page_icon=":material/terminal:", layout="wide")
    st.title("Parser :red[:material/terminal:]")

    notes_dir = os.path.join(os.path.dirname(__file__), 'notes')
    last_ran_parser = get_last_ran_parser()
    if last_ran_parser == "never":
        last_ran_dt = None
    else:
        try:
            last_ran_dt = datetime.strptime(last_ran_parser, "%Y-%m-%d %H:%M:%S")
        except Exception:
            last_ran_dt = None

    files_to_parse = []
    total_size = 0
    file_list = os.listdir(notes_dir)
    for fname in file_list:
        fpath = os.path.join(notes_dir, fname)
        if os.path.isfile(fpath):
            size_bytes = os.path.getsize(fpath)
            # Include all files for parsing
            files_to_parse.append({
                'name': fname,
                'size_bytes': size_bytes
            })
            total_size += size_bytes

    st.write(f"Total Files To Be Parsed: {len(files_to_parse)}")
    if total_size < 1024 * 1024:
        size_str = f"{round(total_size / 1024, 2)} KB"
    else:
        size_str = f"{round(total_size / (1024 * 1024), 2)} MB"
    st.write(f"Total Size: {size_str}")

    # Display files in a collapsible expander instead of dropdown
    file_names = [f['name'] for f in files_to_parse]
    with st.expander("View All Notes To Be Parsed", expanded=False):
        if file_names:
            for fname in file_names:
                st.write(fname)
        else:
            st.write("No files to be parsed.")

    # Dropdown for selecting Ollama Model before parsing
    settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
    with open(settings_path, "r") as f:
        settings = json.load(f)
    # Fetch available models via ollama CLI
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.splitlines()
        available_models = []
        for line in lines:
            parts = line.strip().split()
            if parts and parts[0] not in ("MODEL", "----", "NAME"):
                available_models.append(parts[0])
    except Exception as e:
        st.error(f"Failed to fetch models: {e}")
        available_models = []
    default_model = settings.get("ollama_model", "")
    if available_models:
        default_index = available_models.index(default_model) if default_model in available_models else 0
    else:
        st.warning(
            "At least one model with vision capabilities is required. Recommended: qwen2.5vl:7b"
        )

    # Two dropdowns for selecting Ollama Vision and Linter models
    col1, col2 = st.columns(2)
    with col1:
        default_vis = settings.get("ollama_vision_model", settings.get("ollama_model", ""))
        idx_vis = available_models.index(default_vis) if default_vis in available_models else 0
        selected_vision = st.selectbox(
            "Select Ollama Vision Model:", available_models, index=idx_vis
        )
    with col2:
        default_lint = settings.get("ollama_linter_model", settings.get("ollama_model", ""))
        idx_lint = available_models.index(default_lint) if default_lint in available_models else 0
        selected_linter = st.selectbox(
            "Select Ollama Linter Model:", available_models, index=idx_lint
        )

    # Dummy parse button
    st.button("Parse Files (Dummy)")

if __name__ == "__main__":
    main()

