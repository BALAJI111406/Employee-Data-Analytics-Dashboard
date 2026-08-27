from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """Create an interactive bar chart."""
    return px.bar(df, x=x_col, y=y_col, title=title, color=x_col, template="plotly_white")


def create_pie_chart(df: pd.DataFrame, names: str, values: str, title: str) -> go.Figure:
    """Create a pie chart."""
    return px.pie(df, names=names, values=values, title=title, hole=0.4, template="plotly_white")


def create_histogram(df: pd.DataFrame, column: str, title: str) -> go.Figure:
    """Create a histogram."""
    return px.histogram(df, x=column, title=title, nbins=20, template="plotly_white")


def create_line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """Create a line chart."""
    return px.line(df, x=x_col, y=y_col, title=title, markers=True, template="plotly_white")


def create_box_plot(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """Create a box plot."""
    return px.box(df, x=x_col, y=y_col, title=title, color=x_col, template="plotly_white")


def create_scatter_plot(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """Create a scatter plot."""
    return px.scatter(df, x=x_col, y=y_col, color="Department", title=title, template="plotly_white")


def create_correlation_heatmap(df: pd.DataFrame, numeric_columns: list[str]) -> go.Figure:
    """Create a correlation heatmap for numeric columns."""
    corr = df[numeric_columns].corr(numeric_only=True)
    return px.imshow(corr, title="Correlation Heatmap", template="plotly_white")


def create_department_salary_chart(df: pd.DataFrame) -> go.Figure:
    """Create a department-wise salary average chart."""
    dept_salary = df.groupby("Department")["Salary"].mean().reset_index().sort_values("Salary", ascending=False)
    return px.bar(dept_salary, x="Department", y="Salary", title="Department-wise Average Salary", template="plotly_white")


def create_gender_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Create a gender distribution chart."""
    gender_counts = df["Gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]
    return px.bar(gender_counts, x="Gender", y="Count", title="Gender Distribution", template="plotly_white")


def create_age_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Create an age distribution histogram."""
    return px.histogram(df, x="Age", title="Employee Age Distribution", nbins=15, template="plotly_white")
