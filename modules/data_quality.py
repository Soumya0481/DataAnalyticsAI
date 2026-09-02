import pandas as pd


def get_missing_values(df):
    """Return missing-value information for each column."""

    result = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Missing %": (
            df.isnull().sum().values / len(df) * 100
        ).round(2)
    })

    return result


def get_duplicate_count(df):
    """Return the number of duplicate rows."""

    return int(df.duplicated().sum())


def get_empty_columns(df):
    """Find columns that contain no useful values."""

    empty_columns = []

    for column in df.columns:

        if df[column].isnull().all():
            empty_columns.append(column)

    return empty_columns


def get_unique_values(df):
    """Return unique-value count for each column."""

    result = pd.DataFrame({
        "Column": df.columns,
        "Unique Values": df.nunique(dropna=True).values
    })

    return result


def get_data_health(df):
    """Calculate a simple overall data-health score."""

    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 0

    missing_cells = int(df.isnull().sum().sum())

    duplicate_rows = int(df.duplicated().sum())

    missing_score = (
        1 - (missing_cells / total_cells)
    ) * 100

    duplicate_score = (
        1 - (duplicate_rows / len(df))
    ) * 100

    health_score = (
        missing_score * 0.7
        + duplicate_score * 0.3
    )

    return round(
        max(0, min(100, health_score)),
        2
    )