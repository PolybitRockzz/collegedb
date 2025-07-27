import streamlit as st
import os
import time
import pandas as pd

def get_notes_files(notes_dir):
    files = []
    for fname in os.listdir(notes_dir):
        fpath = os.path.join(notes_dir, fname)
        if os.path.isfile(fpath):
            name, ext = os.path.splitext(fname)
            ext = ext[1:] if ext.startswith('.') else ext
            size = os.path.getsize(fpath)
            mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(fpath)))
            files.append({
                'File Name': name,
                'Extension': ext,
                'Size (bytes)': size,
                'Last Modified': mtime
            })
    return files

def main():
    st.set_page_config(page_title="CollegeDB - Database", page_icon=":material/database:", layout="wide")
    st.title("Database :blue[:material/database:]")

    # Use tabs to switch between raw and parsed notes
    tabs = st.tabs(["Raw Notes", "Parsed Notes"])
    for tab, folder_label in zip(tabs, ["notes", "knowledgebase"]):
        with tab:
            target_dir = os.path.join(os.path.dirname(__file__), folder_label)
            with st.spinner(f'Loading files from {folder_label}...'):
                files = []
                file_list = os.listdir(target_dir)
                total = len(file_list)
                progress = st.progress(0)
                for i, fname in enumerate(file_list):
                    fpath = os.path.join(target_dir, fname)
                    if os.path.isfile(fpath):
                        name, ext = os.path.splitext(fname)
                        ext = ext[1:] if ext.startswith('.') else ext
                        size_bytes = os.path.getsize(fpath)
                        if size_bytes < 1024 * 1024:
                            size = f"{round(size_bytes / 1024, 2)} KB"
                        else:
                            size = f"{round(size_bytes / (1024 * 1024), 2)} MB"
                        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(fpath)))
                        files.append({
                            'File Name': name,
                            'Extension': ext,
                            'Size': size,
                            'Last Modified': mtime
                        })
                    progress.progress((i + 1) / total)
                    time.sleep(0.05)  # Simulate loading
                progress.empty()
            if not files:
                st.warning(f'The {folder_label} folder is empty.')
            else:
                df = pd.DataFrame(files)
                st.dataframe(df)

if __name__ == "__main__":
    main()

