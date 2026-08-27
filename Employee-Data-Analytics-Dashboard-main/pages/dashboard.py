from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.charts import (
    create_age_distribution_chart,
    create_bar_chart,
    create_box_plot,
    create_correlation_heatmap,
    create_department_salary_chart,
    create_gender_distribution_chart,
    create_histogram,
    create_line_chart,
    create_pie_chart,
    create_scatter_plot,
)
from utils.helpers import apply_filters, get_active_dataframe, init_session_state


def render_dashboard_page() -> None:
    """Render the main KPI and visualization dashboard."""
    init_session_state()
    st.title("Executive Dashboard")
    st.markdown("Explore workforce metrics, salary trends, and employee distribution through interactive charts.")

    df = get_active_dataframe()
    if df.empty:
        st.warning("Load a dataset first to view analytics.")
        return

    with st.spinner("Applying filters and preparing the dashboard..."):
        filtered_df = apply_filters(df)

    if filtered_df.empty:
        st.warning("No rows match the current filters.")
        return

    st.subheader("Key Performance Indicators")
    metric_cols = st.columns(6)
    metric_cols[0].metric("Total Employees", len(filtered_df))
    metric_cols[1].metric("Average Salary", f"${filtered_df['Salary'].mean():,.0f}" if "Salary" in filtered_df.columns else "N/A")
    metric_cols[2].metric("Max Salary", f"${filtered_df['Salary'].max():,.0f}" if "Salary" in filtered_df.columns else "N/A")
    metric_cols[3].metric("Min Salary", f"${filtered_df['Salary'].min():,.0f}" if "Salary" in filtered_df.columns else "N/A")
    metric_cols[4].metric("Average Age", round(filtered_df['Age'].mean(), 1) if "Age" in filtered_df.columns else "N/A")
    metric_cols[5].metric("Departments", filtered_df['Department'].nunique() if "Department" in filtered_df.columns else 0)

    st.markdown("---")

    chart_cols = st.columns(2)
    with chart_cols[0]:
        st.plotly_chart(create_pie_chart(filtered_df, "Gender", "Salary", "Gender Distribution"), use_container_width=True)
    with chart_cols[1]:
        st.plotly_chart(create_department_salary_chart(filtered_df), use_container_width=True)

    chart_cols2 = st.columns(2)
    with chart_cols2[0]:
        st.plotly_chart(create_histogram(filtered_df, "Salary", "Salary Distribution"), use_container_width=True)
    with chart_cols2[1]:
        st.plotly_chart(create_age_distribution_chart(filtered_df), use_container_width=True)

    chart_cols3 = st.columns(2)
    with chart_cols3[0]:
        st.plotly_chart(create_bar_chart(filtered_df, "Department", "Salary", "Salary by Department"), use_container_width=True)
    with chart_cols3[1]:
        st.plotly_chart(create_box_plot(filtered_df, "Department", "Salary", "Salary Spread by Department"), use_container_width=True)

    chart_cols4 = st.columns(2)
    with chart_cols4[0]:
        st.plotly_chart(create_scatter_plot(filtered_df, "Experience", "Salary", "Experience vs Salary"), use_container_width=True)
    with chart_cols4[1]:
        if len([c for c in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[c])]) > 1:
            numeric_cols = [c for c in filtered_df.columns if pd.api.types.is_numeric_dtype(filtered_df[c])]
            st.plotly_chart(create_correlation_heatmap(filtered_df, numeric_cols), use_container_width=True)

    st.subheader("Filtered Data Preview")
    st.dataframe(filtered_df.head(15), use_container_width=True)


render_dashboard_page()
