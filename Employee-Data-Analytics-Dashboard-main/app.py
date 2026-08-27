from __future__ import annotations

from pathlib import Path

import streamlit as st

from utils.helpers import ASSETS_PATH, init_session_state, load_base_data


st.set_page_config(
    page_title="Employee Data Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_home_page() -> None:
    """Render the landing page for the application."""
    init_session_state()

    st.markdown(
        """
        <style>
        .block-container { padding-top: 1.2rem; }
        .st-emotion-cache-18e3th9 { padding-top: 0.5rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.2, 0.8])
    with col1:
        st.title("Employee Data Analytics Dashboard")
        st.markdown(
            """
            Welcome to a production-ready analytics experience for exploring employee data, cleaning records,
            and generating business insights with a polished Streamlit interface.
            """
        )
        st.info("Use the sidebar to navigate between upload, cleaning, dashboard, analytics, and reports pages.")

        st.subheader("Highlights")
        st.write(
            "- Upload CSV files or explore the built-in sample dataset\n"
            "- Clean records, handle missing values, and export reports\n"
            "- View dynamic KPIs and interactive charts for decision-making"
        )

    with col2:
        if ASSETS_PATH.exists():
            st.image(str(ASSETS_PATH), width=220)
        else:
            st.image("https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?auto=format&fit=crop&w=600&q=80", width=220)

    st.markdown("---")

    data = load_base_data()
    if data.empty:
        st.warning("No dataset is currently loaded. Use the Upload page to add a CSV file.")
        return

    st.subheader("Quick Overview")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Employees", len(data))
    col_b.metric("Departments", data["Department"].nunique() if "Department" in data.columns else 0)
    col_c.metric("Average Salary", f"${data['Salary'].mean():,.0f}" if "Salary" in data.columns else "N/A")


render_home_page()
