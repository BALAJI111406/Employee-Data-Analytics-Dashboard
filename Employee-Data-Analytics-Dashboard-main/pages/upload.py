from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.helpers import init_session_state, load_base_data


def render_upload_page() -> None:
    """Allow upload of a CSV file and inspect its contents."""
    init_session_state()
    st.title("Dataset Upload")
    st.markdown("Upload a CSV file to replace the built-in sample dataset or inspect a new one.")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
            st.session_state.cleaned_df = None
            st.session_state.uploaded_file_name = uploaded_file.name
            st.success(f"Loaded {uploaded_file.name}")
        except Exception as exc:
            st.error(f"Could not load the file: {exc}")
            return

    data = st.session_state.get("df") if st.session_state.get("df") is not None else load_base_data()

    if data is None or data.empty:
        st.info("No dataset loaded yet. The app will use the bundled sample data by default.")
        return

    st.subheader("Preview")
    st.dataframe(data.head(15), use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", len(data))
    col2.metric("Columns", data.shape[1])
    col3.metric("Loaded File", st.session_state.get("uploaded_file_name") or "sample_data.csv")

    st.subheader("Data Types")
    st.dataframe(data.dtypes.reset_index().rename(columns={"index": "Column", 0: "Data Type"}), use_container_width=True)

    st.subheader("Missing Values")
    missing_summary = pd.DataFrame({
        "Column": data.columns,
        "Missing Values": data.isna().sum(),
        "Missing %": (data.isna().sum() / len(data) * 100).round(2),
    })
    st.dataframe(missing_summary, use_container_width=True)


render_upload_page()
