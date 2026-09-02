import pandas as pd


def get_column_information(df):
    """Return information about every column."""

    information = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Missing %": (
            df.isnull().sum().values / len(df) * 100
        ).round(2),
        "Unique Values": df.nunique().values
    })

    return information


def get_numeric_columns(df):
    """Return numerical columns."""

    return df.select_dtypes(include="number").columns.tolist()


def get_categorical_columns(df):
    """Return categorical/text columns."""

    return df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()


def get_statistical_summary(df):
    """Return statistical summary for numerical columns."""

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    return numeric_df.describe().T

def get_value_counts(df, column):
    """Return frequency counts for a categorical column."""

    return (
        df[column]
        .value_counts()
        .reset_index()
        .rename(
            columns={
                "index": column,
                column: "Count"
            }
        )
    )
def get_categorical_distribution(df, column):
    """Return category frequencies for a categorical column."""

    distribution = (
        df[column]
        .value_counts(dropna=False)
        .reset_index()
    )

    distribution.columns = [column, "Count"]

    return distribution

def get_correlation_matrix(df):
    """Calculate correlation between numerical columns."""

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None

    return numeric_df.corr()