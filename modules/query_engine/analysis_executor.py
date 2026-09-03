import pandas as pd


def _clean_numeric(series):
    """Return a numeric series with invalid values removed."""

    return pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()


def _find_numeric_measure(df, plan):
    """
    Find the numerical measure selected by the planner.

    Uses the planned measure first and validates that
    the actual data can be converted to numeric values.
    """

    measure = plan.get("measure")

    # =========================================
    # 1. TRUST THE PLANNED MEASURE
    # =========================================

    if (
        measure
        and measure in df.columns
    ):

        numeric_values = pd.to_numeric(
            df[measure],
            errors="coerce"
        )

        if numeric_values.notna().any():
            return measure

    # =========================================
    # 2. FALLBACK TO PLANNED COLUMNS
    # =========================================

    for column in plan.get(
        "columns",
        []
    ):

        if column not in df.columns:
            continue

        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        if numeric_values.notna().any():
            return column

    return None


def _calculate_basic_statistics(df, column):
    """Calculate standard descriptive statistics."""

    series = _clean_numeric(
        df[column]
    )

    if series.empty:
        return None

    return pd.DataFrame([
        {
            "Count": int(series.count()),
            "Mean": float(series.mean()),
            "Median": float(series.median()),
            "Minimum": float(series.min()),
            "Maximum": float(series.max()),
            "Standard Deviation": float(
                series.std()
            ),
            "Variance": float(
                series.var()
            )
        }
    ])


def _group_and_aggregate(
    df,
    group_by,
    measure,
    aggregation="mean"
):
    """
    Perform a generic grouped aggregation.
    """

    if group_by not in df.columns:
        return None

    if measure not in df.columns:
        return None

    temp = df[
        [group_by, measure]
    ].copy()

    temp[measure] = pd.to_numeric(
        temp[measure],
        errors="coerce"
    )

    temp = temp.dropna(
        subset=[measure]
    )

    if temp.empty:
        return None

    if aggregation == "sum":

        result = (
            temp.groupby(group_by)[measure]
            .sum()
            .reset_index()
        )

    elif aggregation == "count":

        result = (
            temp.groupby(group_by)[measure]
            .count()
            .reset_index()
        )

    elif aggregation == "median":

        result = (
            temp.groupby(group_by)[measure]
            .median()
            .reset_index()
        )

    elif aggregation == "max":

        result = (
            temp.groupby(group_by)[measure]
            .max()
            .reset_index()
        )

    elif aggregation == "min":

        result = (
            temp.groupby(group_by)[measure]
            .min()
            .reset_index()
        )

    else:

        result = (
            temp.groupby(group_by)[measure]
            .mean()
            .reset_index()
        )

    return result


def _calculate_percentage_by_category(
    df,
    group_by
):
    """
    Calculate percentage contribution
    of each category.
    """

    if group_by not in df.columns:
        return None

    counts = (
        df[group_by]
        .value_counts(dropna=False)
    )

    if counts.empty:
        return None

    percentages = (
        counts / counts.sum() * 100
    )

    result = pd.DataFrame({
        group_by: counts.index.astype(str),
        "Count": counts.values,
        "Percentage": percentages.values
    })

    return result


def _calculate_binary_rate(
    df,
    group_by,
    indicator
):
    """
    Calculate the positive rate of a binary
    indicator.

    Overall:

        positive records / valid records * 100

    Grouped:

        positive records in group /
        valid records in group * 100
    """

    if indicator not in df.columns:
        return None

    temp = df.copy()

    temp["_indicator"] = pd.to_numeric(
        temp[indicator],
        errors="coerce"
    )

    temp = temp.dropna(
        subset=["_indicator"]
    )

    if temp.empty:
        return None

    # =========================================
    # OVERALL RATE
    # =========================================

    if not group_by:

        total_records = len(temp)

        positive_records = int(
            (temp["_indicator"] == 1).sum()
        )

        rate = (
            positive_records
            / total_records
            * 100
        )

        return pd.DataFrame([
            {
                "Metric": "Overall Rate",
                "Total Records": total_records,
                "Positive Records": positive_records,
                "Rate (%)": round(
                    float(rate),
                    2
                )
            }
        ])

    # =========================================
    # GROUPED RATE
    # =========================================

    if group_by not in temp.columns:
        return None

    grouped = (
        temp.groupby(group_by)["_indicator"]
        .agg(
            Total="count",
            Positive=lambda x: int(
                (x == 1).sum()
            )
        )
        .reset_index()
    )

    grouped["Rate (%)"] = (
        grouped["Positive"]
        / grouped["Total"]
        * 100
    )

    grouped["Rate (%)"] = (
        grouped["Rate (%)"]
        .round(2)
    )

    return grouped


def _calculate_distribution(
    df,
    column
):
    """Create a numerical distribution table."""

    if column not in df.columns:
        return None

    series = _clean_numeric(
        df[column]
    )

    if series.empty:
        return None

    bins = min(
        10,
        max(3, series.nunique())
    )

    distribution = (
        pd.cut(
            series,
            bins=bins
        )
        .value_counts(
            sort=False
        )
        .reset_index()
    )

    distribution.columns = [
        "Range",
        "Count"
    ]

    distribution["Range"] = (
        distribution["Range"]
        .astype(str)
    )

    return distribution


def _calculate_correlation(
    df,
    columns
):
    """Calculate correlation between numerical columns."""

    valid_columns = []

    for column in columns:

        if column in df.columns:

            if pd.api.types.is_numeric_dtype(
                df[column]
            ):

                valid_columns.append(
                    column
                )

    if len(valid_columns) < 2:
        return None

    return df[
        valid_columns
    ].corr()


def _calculate_trend(
    df,
    group_by,
    measure=None
):
    """
    Create a time-based or ordered trend.

    If a measure exists, calculate its mean.
    Otherwise count records.
    """

    if group_by not in df.columns:
        return None

    temp = df.copy()

    converted = pd.to_datetime(
        temp[group_by],
        errors="coerce"
    )

    valid_date_ratio = (
        converted.notna().mean()
    )

    if valid_date_ratio < 0.5:

        counts = (
            temp[group_by]
            .value_counts()
            .reset_index()
        )

        counts.columns = [
            group_by,
            "Count"
        ]

        return counts

    temp["_date"] = converted

    temp = temp.dropna(
        subset=["_date"]
    )

    if temp.empty:
        return None

    if (
        measure
        and measure in temp.columns
    ):

        temp[measure] = pd.to_numeric(
            temp[measure],
            errors="coerce"
        )

        temp = temp.dropna(
            subset=[measure]
        )

        result = (
            temp.groupby(
                pd.Grouper(
                    key="_date",
                    freq="ME"
                )
            )[measure]
            .mean()
            .reset_index()
        )

        result.columns = [
            "Date",
            "Value"
        ]

    else:

        result = (
            temp.groupby(
                pd.Grouper(
                    key="_date",
                    freq="ME"
                )
            )
            .size()
            .reset_index(
                name="Count"
            )
        )

        result.columns = [
            "Date",
            "Count"
        ]

    return result


def execute_analysis(
    df,
    plan
):
    """
    Execute a generic analytical plan.

    The function operates on the uploaded
    DataFrame and contains no dataset-specific
    questions.
    """

    result = {
        "data": None,
        "analysis_type": plan.get(
            "intent",
            "analysis"
        ),
        "message": ""
    }

    # =========================================
    # PLAN VALIDATION
    # =========================================

    if plan.get("status") != "ready":

        result["message"] = plan.get(
            "status",
            "The analysis plan is not ready."
        )

        return result

    operations = plan.get(
        "operations",
        []
    )

    group_by = plan.get(
        "group_by"
    )

    measure = _find_numeric_measure(
        df,
        plan
    )

    # =========================================
    # DATASET SUMMARY
    # =========================================

    if "dataset_summary" in operations:

        summary = pd.DataFrame([
            {
                "Rows": len(df),
                "Columns": len(df.columns),
                "Missing Values": int(
                    df.isnull().sum().sum()
                ),
                "Duplicate Rows": int(
                    df.duplicated().sum()
                )
            }
        ])

        result["data"] = summary

        result["analysis_type"] = "summary"

        result["message"] = (
            "Dataset summary generated."
        )

        return result

        # =========================================
    # CORRELATION
    # =========================================

    if "correlation" in operations:

        selected_columns = plan.get(
            "columns",
            []
        )

        # A scatter plot requires exactly
        # two suitable numerical columns.
        if len(selected_columns) < 2:

            result["message"] = (
                "At least two suitable numerical "
                "columns are required for a "
                "scatter plot."
            )

            return result

        selected_columns = selected_columns[:2]

        valid_columns = []

        for column in selected_columns:

            if column not in df.columns:
                continue

            if pd.api.types.is_numeric_dtype(
                df[column]
            ):

                valid_columns.append(
                    column
                )

        if len(valid_columns) < 2:

            result["message"] = (
                "At least two suitable numerical "
                "columns are required for a "
                "scatter plot."
            )

            return result

        scatter_data = df[
            valid_columns
        ].dropna()

        if scatter_data.empty:

            result["message"] = (
                "No valid numerical data is "
                "available for the scatter plot."
            )

            return result

        result["data"] = scatter_data

        result["analysis_type"] = (
            "scatter"
        )

        result["message"] = (
            "Scatter plot data generated."
        )

        return result

    # =========================================
    # TREND
    # =========================================

    if "trend" in operations:

        trend = _calculate_trend(
            df,
            group_by,
            measure
        )

        if trend is None:

            result["message"] = (
                "A suitable time column could "
                "not be analyzed."
            )

            return result

        result["data"] = trend

        result["analysis_type"] = "trend"

        result["message"] = (
            "Trend analysis generated."
        )

        return result

    # =========================================
    # BINARY RATE
    # =========================================

    if (
        "percentage_by_indicator"
        in operations
    ):

        indicator = plan.get(
            "measure"
        )

        # -------------------------------------
        # Make sure the planned indicator
        # actually exists.
        # -------------------------------------

        if (
            not indicator
            or indicator not in df.columns
        ):

            indicator = None

        # -------------------------------------
        # If planner didn't provide one,
        # search for a binary column.
        # -------------------------------------

        if indicator is None:

            for column in plan.get(
                "columns",
                []
            ):

                if column not in df.columns:
                    continue

                values = pd.to_numeric(
                    df[column],
                    errors="coerce"
                ).dropna()

                if values.empty:
                    continue

                unique_values = set(
                    values.unique()
                )

                if unique_values.issubset(
                    {0, 1}
                ):

                    indicator = column
                    break

        # -------------------------------------
        # Last fallback: search dataset.
        # -------------------------------------

        if indicator is None:

            for column in df.columns:

                values = pd.to_numeric(
                    df[column],
                    errors="coerce"
                ).dropna()

                if values.empty:
                    continue

                unique_values = set(
                    values.unique()
                )

                if unique_values.issubset(
                    {0, 1}
                ):

                    indicator = column
                    break

        if indicator is None:

            result["message"] = (
                "No suitable binary indicator "
                "was found."
            )

            return result

        rate = _calculate_binary_rate(
            df,
            group_by,
            indicator
        )

        if rate is None:

            result["message"] = (
                "The requested rate could "
                "not be calculated."
            )

            return result

        result["data"] = rate

        result["analysis_type"] = "rate"

        if group_by:

            result["message"] = (
                "Grouped rate analysis generated."
            )

        else:

            result["message"] = (
                "Overall rate analysis generated."
            )

        return result

        # =========================================
    # COUNT
    # =========================================

    if "count" in operations:

        total_records = len(df)

        result["data"] = pd.DataFrame([
            {
                "Metric": "Total Records",
                "Value": total_records
            }
        ])

        result["analysis_type"] = "count"

        result["message"] = (
            "Record count generated."
        )

        return result


    

    # =========================================
    # COMPARISON
    # =========================================

    if "compare" in operations:

        if (
            group_by
            and measure
        ):

            comparison = _group_and_aggregate(
                df,
                group_by,
                measure,
                "mean"
            )

            if comparison is not None:

                result["data"] = comparison

                result["analysis_type"] = (
                    "comparison"
                )

                result["message"] = (
                    "Comparison analysis generated."
                )

                return result

        if group_by:

            counts = (
                df[group_by]
                .value_counts()
                .reset_index()
            )

            counts.columns = [
                group_by,
                "Count"
            ]

            result["data"] = counts

            result["analysis_type"] = (
                "comparison"
            )

            result["message"] = (
                "Category comparison generated."
            )

            return result

    # =========================================
    # RANKING
    # =========================================

    if "ranking" in operations:

        if not group_by or not measure:

            result["message"] = (
                "A category and numerical "
                "measure are required."
            )

            return result

        ranking = _group_and_aggregate(
            df,
            group_by,
            measure,
            "mean"
        )

        if ranking is None:

            result["message"] = (
                "Ranking could not be calculated."
            )

            return result

        ranking = ranking.sort_values(
            measure,
            ascending=False
        )

        result["data"] = ranking

        result["analysis_type"] = "ranking"

        result["message"] = (
            "Ranking analysis generated."
        )

        return result

    # =========================================
    # PERCENTAGE
    # =========================================

    if "percentage" in operations:

        if not group_by:

            result["message"] = (
                "A categorical column is "
                "required for percentage analysis."
            )

            return result

        percentage = (
            _calculate_percentage_by_category(
                df,
                group_by
            )
        )

        if percentage is None:

            result["message"] = (
                "Percentage analysis failed."
            )

            return result

        result["data"] = percentage

        result["analysis_type"] = (
            "percentage"
        )

        result["message"] = (
            "Percentage analysis generated."
        )

        return result

    # =========================================
    # DISTRIBUTION
    # =========================================

    if "distribution" in operations:

        if not measure:

            result["message"] = (
                "No suitable numerical measure "
                "was found."
            )

            return result

        distribution = _calculate_distribution(
            df,
            measure
        )

        if distribution is None:

            result["message"] = (
                "Distribution could not be calculated."
            )

            return result

        result["data"] = distribution

        result["analysis_type"] = (
            "distribution"
        )

        result["message"] = (
            "Distribution analysis generated."
        )

        return result

    # =========================================
    # CATEGORICAL DISTRIBUTION
    # =========================================

    if (
        "categorical_distribution"
        in operations
    ):

        if not group_by:

            result["message"] = (
                "No categorical column was found."
            )

            return result

        distribution = (
            df[group_by]
            .value_counts(dropna=False)
            .reset_index()
        )

        distribution.columns = [
            group_by,
            "Count"
        ]

        result["data"] = distribution

        result["analysis_type"] = (
            "categorical_distribution"
        )

        result["message"] = (
            "Categorical distribution generated."
        )

        return result

    # =========================================
    # STATISTICS
    # =========================================

    if "statistical_analysis" in operations:

        if not measure:

            result["message"] = (
                "No suitable numerical column "
                "was found."
            )

            return result

        statistics = (
            _calculate_basic_statistics(
                df,
                measure
            )
        )

        if statistics is None:

            result["message"] = (
                "Statistics could not be calculated."
            )

            return result

        result["data"] = statistics

        result["analysis_type"] = (
            "statistics"
        )

        result["message"] = (
            "Statistical analysis generated."
        )

        return result
        # =========================================
    # DIRECT NUMERICAL STATISTICS
    # =========================================

    if operations:

        direct_operations = [
            "max",
            "min",
            "median",
            "sum"
        ]

        for operation in direct_operations:

            if operation not in operations:
                continue

            if not measure:

                result["message"] = (
                    "No suitable numerical measure "
                    "was found."
                )

                return result

            if measure not in df.columns:

                result["message"] = (
                    "The selected measure was not "
                    "found in the dataset."
                )

                return result

            series = _clean_numeric(
                df[measure]
            )

            if series.empty:

                result["message"] = (
                    "The selected column does not "
                    "contain usable numerical values."
                )

                return result

            if operation == "max":

                value = float(
                    series.max()
                )

                label = "Maximum"

            elif operation == "min":

                value = float(
                    series.min()
                )

                label = "Minimum"

            elif operation == "median":

                value = float(
                    series.median()
                )

                label = "Median"

            elif operation == "sum":

                value = float(
                    series.sum()
                )

                label = "Total"

            result["data"] = pd.DataFrame([
                {
                    "Measure": measure,
                    "Metric": label,
                    "Value": value
                }
            ])

            result["analysis_type"] = (
                "statistics"
            )

            result["message"] = (
                f"{label} analysis generated."
            )

            return result
    # =========================================
    # FALLBACK
    # =========================================

    result["message"] = (
        "The requested analysis could not "
        "be performed with the available data."
    )

    return result