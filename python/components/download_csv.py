import streamlit as st

def download_button(selected_csv_path: str):
    with open(selected_csv_path, "rb") as f:
        st.download_button("Download CSV", f, "log.csv", "text/csv")