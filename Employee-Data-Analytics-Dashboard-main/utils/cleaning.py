from __future__ import annotations

from typing import Any

import pandas as pd


def clean_dataframe(
    df: pd.DataFrame,
    remove_duplicates: bool = True,
    missing_strategy: str = "median",
    rename_map: dict[str, str] | None = None,
    columns_to_drop: list[str] | None = None,
    convert_dates: bool = True,
) -> pd.DataFrame:
    """Clean and standardize the incoming dataframe."""
    cleaned = df.copy()

    if cleaned.empty:
        return cleaned

    if remove_duplicates:
        cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    if rename_map:
        cleaned = cleaned.rename(columns=rename_map)

    if columns_to_drop:
        cleaned = cleaned.drop(columns=[c for c in columns_to_drop if c in cleaned.columns], errors="ignore")

    if convert_dates:
        for column in cleaned.columns:
            if "date" in column.lower():
                cleaned[column] = pd.to_datetime(cleaned[column], errors="coerce")

    if missing_strategy == "delete":
        cleaned = cleaned.dropna()
        return cleaned

    for column in cleaned.columns:
        if cleaned[column].isna().any():
            if pd.api.types.is_numeric_dtype(cleaned[column]):
                if missing_strategy == "mean":
                    fill_value = cleaned[column].mean()
                elif missing_strategy == "median":
                    fill_value = cleaned[column].median()
                else:
                    fill_value = cleaned[column].mode().iloc[0] if not cleaned[column].mode().empty else 0
                cleaned[column] = cleaned[column].fillna(fill_value)
            else:
                fill_value = cleaned[column].mode().iloc[0] if not cleaned[column].mode().empty else "Unknown"
                cleaned[column] = cleaned[column].fillna(fill_value)

    return cleaned


def summarize_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize missing values by column."""
    return pd.DataFrame({"Column": df.columns, "Missing": df.isna().sum(), "MissingPct": (df.isna().sum() / len(df) * 100).round(2)})


def detect_date_columns(df: pd.DataFrame) -> list[str]:
    """Return columns likely to contain dates."""
    return [column for column in df.columns if "date" in column.lower()]
