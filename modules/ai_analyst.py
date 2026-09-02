def generate_ai_analysis(
    df,
    insights,
    anomalies,
    correlation_matrix
):
    """
    Generate a consolidated analyst-style report
    from the existing analytics results.
    """

    analysis = {
        "overview": "",
        "data_quality": "",
        "patterns": [],
        "relationships": [],
        "anomalies": "",
        "reliability": [],
        "recommendations": []
    }

    # =========================================
    # OVERVIEW
    # =========================================

    rows = len(df)
    columns = len(df.columns)

    analysis["overview"] = (
        f"The dataset contains {rows} records "
        f"across {columns} columns."
    )


    # =========================================
    # DATA RELIABILITY
    # =========================================

    if rows < 10:

        analysis["reliability"].append(
            f"⚠️ This dataset contains only {rows} "
            "records. Statistical patterns and "
            "relationships may not be reliable. "
            "More data would provide stronger "
            "conclusions."
        )

    elif rows < 50:

        analysis["reliability"].append(
            f"ℹ️ This dataset contains {rows} records. "
            "Some statistical findings should be "
            "interpreted with caution."
        )

    else:

        analysis["reliability"].append(
            "✅ The dataset contains a reasonable "
            "number of records for exploratory analysis."
        )


    # =========================================
    # DATA QUALITY
    # =========================================

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )


    if missing_values == 0 and duplicate_rows == 0:

        analysis["data_quality"] = (
            "The dataset has no missing values "
            "or duplicate records."
        )

    elif missing_values > 0 and duplicate_rows == 0:

        analysis["data_quality"] = (
            f"The dataset contains {missing_values} "
            "missing values, but no duplicate records."
        )

    elif missing_values == 0 and duplicate_rows > 0:

        analysis["data_quality"] = (
            f"The dataset contains {duplicate_rows} "
            "duplicate records, but no missing values."
        )

    else:

        analysis["data_quality"] = (
            f"The dataset contains {missing_values} "
            f"missing values and {duplicate_rows} "
            "duplicate records."
        )


    # =========================================
    # PATTERNS
    # =========================================

    if insights.get("patterns"):

        analysis["patterns"].extend(
            insights["patterns"]
        )


    # =========================================
    # CATEGORY INSIGHTS
    # =========================================

    if insights.get("categories"):

        analysis["patterns"].extend(
            insights["categories"]
        )


    # =========================================
    # RELATIONSHIPS
    # =========================================

    if correlation_matrix is not None:

        numeric_columns = (
            correlation_matrix.columns.tolist()
        )

        strongest_pair = None
        strongest_value = 0

        for i in range(len(numeric_columns)):

            for j in range(
                i + 1,
                len(numeric_columns)
            ):

                column_1 = numeric_columns[i]
                column_2 = numeric_columns[j]

                value = correlation_matrix.loc[
                    column_1,
                    column_2
                ]

                if abs(value) > abs(strongest_value):

                    strongest_value = value

                    strongest_pair = (
                        column_1,
                        column_2
                    )


        if strongest_pair is not None:

            column_1, column_2 = strongest_pair

            if abs(strongest_value) >= 0.8:

                strength = "strong"

            elif abs(strongest_value) >= 0.5:

                strength = "moderate"

            elif abs(strongest_value) >= 0.3:

                strength = "weak"

            else:

                strength = "very weak"


            direction = (
                "positive"
                if strongest_value > 0
                else "negative"
            )


            analysis["relationships"].append(
                f"{column_1} and {column_2} show a "
                f"{strength} {direction} relationship "
                f"(correlation: {strongest_value:.2f})."
            )


    # =========================================
    # ANOMALIES
    # =========================================

    if anomalies is None or anomalies.empty:

        analysis["anomalies"] = (
            "No potential numerical anomalies "
            "were detected."
        )

    else:

        analysis["anomalies"] = (
            f"{len(anomalies)} potential anomalies "
            "were detected and should be reviewed."
        )


    # =========================================
    # RECOMMENDATIONS
    # =========================================

    if missing_values > 0:

        analysis["recommendations"].append(
            "Review and handle missing values "
            "before further analysis."
        )


    if duplicate_rows > 0:

        analysis["recommendations"].append(
            "Review duplicate records to determine "
            "whether they should be removed."
        )


    if anomalies is not None and not anomalies.empty:

        analysis["recommendations"].append(
            "Investigate the detected anomalies "
            "before making decisions."
        )


    if correlation_matrix is not None:

        analysis["recommendations"].append(
            "Investigate important relationships "
            "to understand potential patterns."
        )


    if rows < 10:

        analysis["recommendations"].append(
            "Add more records before making important "
            "decisions based on this analysis."
        )


    if not analysis["recommendations"]:

        analysis["recommendations"].append(
            "The dataset appears suitable for "
            "further exploratory analysis."
        )


    return analysis