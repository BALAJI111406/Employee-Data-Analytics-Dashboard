from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.helpers import apply_filters, get_active_dataframe, init_session_state


def render_analytics_page() -> None:
    """Render advanced analytics and employee insights."""
    init_session_state()
    st.title("Advanced Analytics")
    st.markdown("Deep-dive into compensation, tenure, and growth patterns.")

    df = get_active_dataframe()
    if df.empty:
        st.warning("Load a dataset first.")
        return

    with st.spinner("Running advanced analytics..."):
        filtered_df = apply_filters(df)
    if filtered_df.empty:
        st.warning("No rows match the current filters.")
        return

    if "Salary" in filtered_df.columns:
        highest_paid = filtered_df.loc[filtered_df["Salary"].idxmax()]
        lowest_paid = filtered_df.loc[filtered_df["Salary"].idxmin()]
        top_10 = filtered_df.nlargest(10, "Salary")
        dept_avg = filtered_df.groupby("Department")["Salary"].mean().reset_index().sort_values("Salary", ascending=False)
    else:
        highest_paid = pd.Series({"Name": "N/A", "Salary": "N/A"})
        lowest_paid = pd.Series({"Name": "N/A", "Salary": "N/A"})
        top_10 = filtered_df.head(10)
        dept_avg = pd.DataFrame(columns=["Department", "Salary"])

    st.subheader("Key Insights")
    insight_cols = st.columns(4)
    insight_cols[0].metric("Highest Paid Employee", highest_paid.get("Name", "N/A"))
    insight_cols[1].metric("Lowest Paid Employee", lowest_paid.get("Name", "N/A"))
    insight_cols[2].metric("Top 10 Salaries", len(top_10))
    insight_cols[3].metric("Departments Reviewed", filtered_df["Department"].nunique() if "Department" in filtered_df.columns else 0)

    st.subheader("Top 10 Salaries")
    st.dataframe(top_10[["Employee_ID", "Name", "Department", "Salary"]].head(10), use_container_width=True)

    st.subheader("Department-wise Salary Average")
    st.dataframe(dept_avg, use_container_width=True)

    st.subheader("Experience Analysis")
    if "Experience" in filtered_df.columns:
        exp_summary = filtered_df.groupby("Department")["Experience"].mean().reset_index().sort_values("Experience", ascending=False)
        st.dataframe(exp_summary, use_container_width=True)

    st.subheader("Employee Growth by Year")
    if "Join_Date" in filtered_df.columns:
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy["Join_Date"] = pd.to_datetime(filtered_df_copy["Join_Date"], errors="coerce")
        growth = filtered_df_copy.dropna(subset=["Join_Date"]).groupby(filtered_df_copy["Join_Date"].dt.year).size().reset_index(name="Count")
        growth.columns = ["Join_Year", "Employee_Count"]
        st.dataframe(growth, use_container_width=True)


render_analytics_page()
