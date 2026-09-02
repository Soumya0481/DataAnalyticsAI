import pandas as pd


def is_sensitive_or_identifier(column_name):
    """
    Check whether a column looks like an email,
    phone number, ID, or other identifier.
    """

    name = str(column_name).lower().strip()

    sensitive_keywords = [
        "email",
        "gmail",
        "mail",
        "phone",
        "mobile",
        "contact",
        "password",
        "pass",
        "user id",
        "userid",
        "customer id",
        "customerid",
        "student id",
        "studentid",
        "employee id",
        "employeeid",
        "account id",
        "accountid"
    ]

    for keyword in sensitive_keywords:

        if keyword in name:
            return True

    return False


def generate_insights(df):
    """Generate categorized insights from the dataset."""

    insights = {
        "summary": [],
        "quality": [],
        "patterns": [],
        "categories": [],
        "relationships": []
    }

    # =========================================
    # DATASET SUMMARY
    # =========================================

    rows = len(df)
    columns = len(df.columns)

    insights["summary"].append(
        f"Your dataset contains {rows} records "
        f"and {columns} columns."
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

    if missing_values == 0:

        insights["quality"].append(
            "No missing values were detected "
            "in the dataset."
        )

    else:

        insights["quality"].append(
            f"The dataset contains {missing_values} "
            "missing values that may need attention."
        )

    if duplicate_rows == 0:

        insights["quality"].append(
            "No duplicate records were detected."
        )

    else:

        insights["quality"].append(
            f"{duplicate_rows} duplicate records "
            "were detected."
        )

    # =========================================
    # NUMERICAL ANALYSIS
    # =========================================

    numeric_columns = [
        column
        for column in df.select_dtypes(
            include="number"
        ).columns
        if not is_sensitive_or_identifier(column)
    ]

    if numeric_columns:

        insights["patterns"].append(
            f"The dataset contains "
            f"{len(numeric_columns)} numerical columns "
            "available for analysis."
        )

        if len(numeric_columns) > 1:

            standard_deviations = (
                df[numeric_columns]
                .std()
                .sort_values(ascending=False)
            )

            highest_variation = (
                standard_deviations.index[0]
            )

            lowest_variation = (
                standard_deviations.index[-1]
            )

            insights["patterns"].append(
                f"'{highest_variation}' shows the "
                "highest variation among the numerical "
                "columns."
            )

            insights["patterns"].append(
                f"'{lowest_variation}' shows the "
                "lowest variation among the numerical "
                "columns."
            )

    # =========================================
    # CATEGORICAL ANALYSIS
    # =========================================

    categorical_columns = [
        column
        for column in df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns
        if not is_sensitive_or_identifier(column)
    ]

    if categorical_columns:

        insights["categories"].append(
            f"The dataset contains "
            f"{len(categorical_columns)} categorical "
            "columns available for analysis."
        )

        # -----------------------------------------
        # DOMINANT CATEGORIES
        # -----------------------------------------

        for column in categorical_columns:

            value_counts = (
                df[column]
                .value_counts(dropna=True)
            )

            if value_counts.empty:
                continue

            dominant_value = value_counts.index[0]

            dominant_count = value_counts.iloc[0]

            percentage = (
                dominant_count / len(df)
            ) * 100

            if percentage >= 50:

                insights["categories"].append(
                    f"In '{column}', "
                    f"'{dominant_value}' is the most "
                    f"common category, representing "
                    f"{percentage:.1f}% of the records."
                )

    # =========================================
    # CORRELATION / RELATIONSHIPS
    # =========================================

    if len(numeric_columns) >= 2:

        correlation_matrix = (
            df[numeric_columns]
            .corr()
        )

        strongest_relationship = None
        strongest_value = 0

        for i in range(len(numeric_columns)):

            for j in range(
                i + 1,
                len(numeric_columns)
            ):

                column_1 = numeric_columns[i]
                column_2 = numeric_columns[j]

                correlation = correlation_matrix.loc[
                    column_1,
                    column_2
                ]

                if pd.isna(correlation):
                    continue

                if abs(correlation) > abs(strongest_value):

                    strongest_value = correlation

                    strongest_relationship = (
                        column_1,
                        column_2
                    )

        if strongest_relationship is not None:

            column_1, column_2 = (
                strongest_relationship
            )

            strength = abs(strongest_value)

            if strength >= 0.8:

                relationship_strength = "strong"

            elif strength >= 0.5:

                relationship_strength = "moderate"

            elif strength >= 0.3:

                relationship_strength = "weak"

            else:

                relationship_strength = "very weak"

            direction = (
                "positive"
                if strongest_value > 0
                else "negative"
            )

            insights["relationships"].append(
                f"'{column_1}' and '{column_2}' "
                f"show a {relationship_strength} "
                f"{direction} relationship "
                f"(correlation: {strongest_value:.2f})."
            )

    return insights