from __future__ import annotations

import io

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from matplotlib.backends.backend_pdf import PdfPages

from utils.helpers import get_active_dataframe, init_session_state


def render_reports_page() -> None:
    """Allow users to export cleaned data and generate a simple summary report."""
    init_session_state()
    st.title("Reports & Export")
    st.markdown("Export the current dataset or generate a business summary report.")

    df = get_active_dataframe()
    if df.empty:
        st.warning("Load or upload a dataset first.")
        return

    st.subheader("Export Data")
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv_bytes, file_name="employee_report.csv", mime="text/csv")

    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Employees", index=False)
    excel_bytes = excel_buffer.getvalue()
    st.download_button("Download Excel Report", excel_bytes, file_name="employee_report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.subheader("PDF Summary")
    summary_text = (
        f"Employee Summary\n"
        f"Total Employees: {len(df)}\n"
        f"Average Salary: ${df['Salary'].mean():,.0f}\n"
        f"Highest Salary: ${df['Salary'].max():,.0f}\n"
        f"Departments: {df['Department'].nunique() if 'Department' in df.columns else 0}"
        if "Salary" in df.columns
        else f"Employee Summary\nTotal Employees: {len(df)}"
    )
    pdf_buffer = io.BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis("off")
        ax.text(0.05, 0.95, summary_text, ha="left", va="top", fontsize=12, family="monospace")
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
    pdf_bytes = pdf_buffer.getvalue()
    st.download_button("Download PDF Summary", pdf_bytes, file_name="employee_summary.pdf", mime="application/pdf")

    st.download_button("Download Summary Text", summary_text, file_name="employee_summary.txt")


render_reports_page()
