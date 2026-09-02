def find_column(df, question):
    """Find a dataset column mentioned in the question."""

    question_lower = question.lower()

    for column in df.columns:

        column_name = str(column).lower()

        if column_name in question_lower:
            return column

    return None


def answer_data_question(df, question):
    """Answer natural-language questions about the dataset."""

    question = question.lower().strip()

    if not question:
        return "Please enter a question about your dataset."

    selected_column = find_column(df, question)

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    # =========================================
    # DATASET SUMMARY
    # =========================================

    if (
        "tell me about" in question
        or "describe the dataset" in question
        or "describe my data" in question
        or "give me a summary" in question
        or "dataset summary" in question
        or "summarize" in question
        or "overall summary" in question
        or "what do you know about" in question
    ):

        missing = int(
            df.isnull().sum().sum()
        )

        duplicates = int(
            df.duplicated().sum()
        )

        return (
            f"Your dataset contains {len(df)} records "
            f"and {len(df.columns)} columns. "
            f"It has {len(numeric_columns)} numerical "
            f"columns and {len(categorical_columns)} "
            f"categorical columns. "
            f"There are {missing} missing values and "
            f"{duplicates} duplicate records."
        )

    # =========================================
    # ROWS / RECORDS
    # =========================================

    if (
        "how many rows" in question
        or "how much row" in question
        or "number of rows" in question
        or "how many records" in question
        or "number of records" in question
        or "how many entries" in question
        or "how many data" in question
    ):

        return (
            f"Your dataset contains {len(df)} records."
        )

    # =========================================
    # COLUMNS
    # =========================================

    if (
        "how many columns" in question
        or "number of columns" in question
        or "how many fields" in question
    ):

        return (
            f"Your dataset contains "
            f"{len(df.columns)} columns."
        )

    # =========================================
    # LIST COLUMNS
    # =========================================

    if (
        "what columns" in question
        or "list columns" in question
        or "column names" in question
        or "which columns" in question
        or "show columns" in question
    ):

        columns = ", ".join(
            str(column)
            for column in df.columns
        )

        return (
            f"Your dataset contains these columns: "
            f"{columns}"
        )

    # =========================================
    # NUMERICAL COLUMNS
    # =========================================

    if (
        "numerical columns" in question
        or "numeric columns" in question
        or "number columns" in question
    ):

        if numeric_columns:

            columns = ", ".join(
                str(column)
                for column in numeric_columns
            )

            return (
                f"The numerical columns are: "
                f"{columns}"
            )

        return "There are no numerical columns."

    # =========================================
    # CATEGORICAL COLUMNS
    # =========================================

    if (
        "categorical columns" in question
        or "category columns" in question
    ):

        if categorical_columns:

            columns = ", ".join(
                str(column)
                for column in categorical_columns
            )

            return (
                f"The categorical columns are: "
                f"{columns}"
            )

        return "There are no categorical columns."

    # =========================================
    # MISSING VALUES
    # =========================================

    if (
        "missing" in question
        or "null" in question
        or "empty values" in question
    ):

        if selected_column is not None:

            missing = int(
                df[selected_column].isnull().sum()
            )

            return (
                f"'{selected_column}' contains "
                f"{missing} missing values."
            )

        missing = int(
            df.isnull().sum().sum()
        )

        if missing == 0:

            return (
                "Your dataset does not contain "
                "any missing values."
            )

        return (
            f"Your dataset contains {missing} "
            "missing values."
        )

    # =========================================
    # DUPLICATES
    # =========================================

    if (
        "duplicate" in question
        or "duplicated" in question
    ):

        duplicates = int(
            df.duplicated().sum()
        )

        if duplicates == 0:

            return (
                "Your dataset does not contain "
                "duplicate records."
            )

        return (
            f"Your dataset contains "
            f"{duplicates} duplicate records."
        )

    # =========================================
    # AVERAGE
    # =========================================

    if (
        "average" in question
        or "mean" in question
        or "avg" in question
    ):

        if selected_column in numeric_columns:

            value = df[selected_column].mean()

            return (
                f"The average {selected_column} "
                f"is {value:.2f}."
            )

        return (
            "Please mention a numerical column. "
            "For example: What is the average Age?"
        )

    # =========================================
    # HIGHEST VALUE
    # =========================================

    if (
        "highest" in question
        or "maximum" in question
        or "max" in question
        or "largest" in question
    ):

        if selected_column in numeric_columns:

            value = df[selected_column].max()

            return (
                f"The highest value of "
                f"{selected_column} is {value}."
            )

        return (
            "Please mention a numerical column "
            "for the highest value."
        )

    # =========================================
    # LOWEST VALUE
    # =========================================

    if (
        "lowest" in question
        or "minimum" in question
        or "min" in question
        or "smallest" in question
    ):

        if selected_column in numeric_columns:

            value = df[selected_column].min()

            return (
                f"The lowest value of "
                f"{selected_column} is {value}."
            )

        return (
            "Please mention a numerical column "
            "for the lowest value."
        )

    # =========================================
    # UNIQUE VALUES
    # =========================================

    if (
        "unique" in question
        or "different values" in question
        or "how many categories" in question
    ):

        if selected_column is not None:

            count = df[selected_column].nunique()

            return (
                f"'{selected_column}' contains "
                f"{count} unique values."
            )

        return (
            "Please mention the column you want "
            "to check."
        )

    # =========================================
    # MOST COMMON VALUE
    # =========================================

    if (
        "most common" in question
        or "most frequent" in question
        or "majority" in question
    ):

        if selected_column is not None:

            counts = (
                df[selected_column]
                .value_counts(dropna=True)
            )

            if not counts.empty:

                value = counts.index[0]
                count = counts.iloc[0]

                return (
                    f"The most common value in "
                    f"'{selected_column}' is "
                    f"'{value}', appearing "
                    f"{count} times."
                )

        return (
            "Please mention the column you want "
            "to analyze."
        )

    # =========================================
    # FALLBACK
    # =========================================

    return (
        "I couldn't understand that question yet. "
        "Try asking about your dataset summary, "
        "rows, columns, numerical columns, "
        "categorical columns, missing values, "
        "duplicates, averages, highest values, "
        "lowest values, or common categories."
    )