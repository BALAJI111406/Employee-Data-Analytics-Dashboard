from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.cleaning import clean_dataframe, detect_date_columns, summarize_missing_values
from utils.helpers import get_active_dataframe, init_session_state


def render_cleaning_page() -> None:
    """Provide a no-code cleaning workflow for uploaded or sample data."""
    init_session_state()
    st.title("Data Cleaning")
    st.markdown("Clean, transform, and prepare your dataset before analysis.")

    df = get_active_dataframe()
    if df.empty:
        st.warning("Load or upload a dataset first.")
        return

    st.subheader("Current Dataset")
    st.dataframe(df.head(10), use_container_width=True)

    with st.sidebar:
        st.subheader("Cleaning Options")
        remove_duplicates = st.checkbox("Remove duplicate rows", value=True)
        missing_strategy = st.selectbox("Missing values strategy", ["median", "mean", "mode", "delete"])
        convert_dates = st.checkbox("Auto-convert date columns", value=True)
        rename_map_text = st.text_area(
            "Rename columns (old:new, one per line)",
            value="",
            help="Example: Employee_ID:EmployeeID",
        )
        drop_columns_text = st.text_area("Columns to remove (one per line)", value="")

    if st.button("Apply Cleaning"):
        rename_map = {}
        if rename_map_text.strip():
            for line in rename_map_text.splitlines():
                if ":" in line:
                    old, new = [item.strip() for item in line.split(":", 1)]
                    rename_map[old] = new

        columns_to_drop = [item.strip() for item in drop_columns_text.splitlines() if item.strip()]

        cleaned = clean_dataframe(
            df,
            remove_duplicates=remove_duplicates,
            missing_strategy=missing_strategy,
            rename_map=rename_map,
            columns_to_drop=columns_to_drop,
            convert_dates=convert_dates,
        )
        st.session_state.cleaned_df = cleaned
        st.success("Cleaning completed successfully.")

    cleaned = st.session_state.get("cleaned_df") if st.session_state.get("cleaned_df") is not None else df

    st.subheader("Cleaning Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", len(cleaned))
    col2.metric("Columns", cleaned.shape[1])
    col3.metric("Date Columns", len(detect_date_columns(cleaned)))

    st.subheader("Missing Values Summary")
    st.dataframe(summarize_missing_values(cleaned), use_container_width=True)

    st.subheader("Cleaned Preview")
    st.dataframe(cleaned.head(12), use_container_width=True)

    csv_data = cleaned.to_csv(index=False).encode("utf-8")
    st.download_button("Download Cleaned CSV", csv_data, file_name="cleaned_employee_data.csv", mime="text/csv")


render_cleaning_page()
