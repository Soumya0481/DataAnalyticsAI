import pandas as pd


def detect_anomalies(df):
    """
    Detect unusual values in numerical columns
    using the IQR method.
    """

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    anomalies = []

    for column in numeric_columns:

        data = df[column].dropna()

        if len(data) < 4:
            continue

        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        unusual_values = data[
            (data < lower_bound) |
            (data > upper_bound)
        ]

        for index, value in unusual_values.items():

            anomalies.append({
                "Row": index + 1,
                "Column": column,
                "Value": value,
                "Expected Minimum": round(
                    lower_bound, 2
                ),
                "Expected Maximum": round(
                    upper_bound, 2
                )
            })

    return pd.DataFrame(anomalies)