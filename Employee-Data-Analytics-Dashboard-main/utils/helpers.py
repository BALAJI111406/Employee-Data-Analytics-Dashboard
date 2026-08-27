from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "dataset" / "employee_data.csv"
ASSETS_PATH = PROJECT_ROOT / "assets" / "logo.png"


def init_session_state() -> None:
    """Initialize the session state with default app values."""
    defaults: dict[str, Any] = {
        "df": None,
        "cleaned_df": None,
        "uploaded_file_name": None,
        "theme_mode": "light",
        "search_type": "Employee ID",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_base_data() -> pd.DataFrame:
    """Load the packaged sample dataset if it exists."""
    if DATASET_PATH.exists():
        return pd.read_csv(DATASET_PATH)
    return pd.DataFrame()


def get_active_dataframe() -> pd.DataFrame:
    """Return the cleaned dataframe if available, otherwise the uploaded or base dataframe."""
    if st.session_state.get("cleaned_df") is not None:
        return st.session_state.cleaned_df
    if st.session_state.get("df") is not None:
        return st.session_state.df
    return load_base_data()


def render_theme_toggle() -> None:
    """Render a simple light/dark toggle in the sidebar."""
    theme_choice = st.sidebar.radio(
        "Theme",
        ["light", "dark"],
        index=0 if st.session_state.get("theme_mode", "light") == "light" else 1,
        horizontal=False,
    )
    st.session_state.theme_mode = theme_choice

    if theme_choice == "dark":
        st.markdown(
            """
            <style>
            .stApp { background-color: #0f172a; color: #f8fafc; }
            .stSidebar { background-color: #111827; }
            div[data-testid="stMetric"] { background-color: #111827; border-radius: 10px; }
            </style>
            """,
            unsafe_allow_html=True,
        )


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sidebar filters and search controls to a dataframe."""
    if df.empty:
        return df

    filtered = df.copy()

    st.sidebar.markdown("### Search")
    search_type = st.sidebar.selectbox("Search By", ["Employee ID", "Name", "Department"], key="search_type")
    search_query = st.sidebar.text_input("Search Term", placeholder="Type keyword")

    if search_query:
        search_query = search_query.strip().lower()
        if search_type == "Employee ID":
            filtered = filtered[filtered["Employee_ID"].astype(str).str.contains(search_query, case=False, na=False)]
        elif search_type == "Name":
            filtered = filtered[filtered["Name"].astype(str).str.contains(search_query, case=False, na=False)]
        else:
            filtered = filtered[filtered["Department"].astype(str).str.contains(search_query, case=False, na=False)]

    department = st.sidebar.selectbox("Department", ["All", *sorted(filtered["Department"].dropna().astype(str).unique())])
    gender = st.sidebar.selectbox("Gender", ["All", *sorted(filtered["Gender"].dropna().astype(str).unique())])

    if "Salary" in filtered.columns:
        salary_min = int(filtered["Salary"].dropna().min())
        salary_max = int(filtered["Salary"].dropna().max())
        salary_range = st.sidebar.slider("Salary Range", salary_min, salary_max, (salary_min, salary_max))
        filtered = filtered[(filtered["Salary"].between(salary_range[0], salary_range[1]))]

    if "Age" in filtered.columns:
        age_min = int(filtered["Age"].dropna().min())
        age_max = int(filtered["Age"].dropna().max())
        age_range = st.sidebar.slider("Age Range", age_min, age_max, (age_min, age_max))
        filtered = filtered[filtered["Age"].between(age_range[0], age_range[1])]

    if "Experience" in filtered.columns:
        exp_min = int(filtered["Experience"].dropna().min())
        exp_max = int(filtered["Experience"].dropna().max())
        exp_range = st.sidebar.slider("Experience", exp_min, exp_max, (exp_min, exp_max))
        filtered = filtered[filtered["Experience"].between(exp_range[0], exp_range[1])]

    if "Join_Date" in filtered.columns:
        join_years = sorted(pd.to_datetime(filtered["Join_Date"], errors="coerce").dt.year.dropna().astype(int).unique())
        if join_years:
            join_year = st.sidebar.selectbox("Joining Year", ["All", *join_years])
            if join_year != "All":
                filtered = filtered[pd.to_datetime(filtered["Join_Date"], errors="coerce").dt.year == join_year]

    if department != "All":
        filtered = filtered[filtered["Department"].astype(str) == department]
    if gender != "All":
        filtered = filtered[filtered["Gender"].astype(str) == gender]

    return filtered
