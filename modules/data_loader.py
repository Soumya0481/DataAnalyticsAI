import pandas as pd


def load_data(uploaded_file):
    """Load CSV or Excel file into a DataFrame."""

    if uploaded_file.name.lower().endswith(".csv"):
        return pd.read_csv(uploaded_file)

    elif uploaded_file.name.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)

    else:
        raise ValueError("Unsupported file format")


def get_data_quality(df):
    """Generate basic data-quality information."""

    quality = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }

    return quality