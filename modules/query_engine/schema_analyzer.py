import pandas as pd


def _detect_column_role(column_name, series):
    """
    Infer a general analytical role for a column.

    This is based on column characteristics, not
    individual user questions.
    """

    name = str(column_name).lower().strip()

    non_null = series.dropna()

    # =========================================
    # BOOLEAN
    # =========================================

    unique_values = set(
        str(value).lower()
        for value in non_null.unique()
    )

    if unique_values and unique_values.issubset(
        {"true", "false", "yes", "no", "0", "1"}
    ):

        return "binary"

    # =========================================
    # DATE / TIME
    # =========================================

    if pd.api.types.is_datetime64_any_dtype(series):

        return "date"

    converted = pd.to_datetime(
        non_null,
        errors="coerce"
    )

    if len(non_null) > 0:

        valid_ratio = converted.notna().mean()

        if valid_ratio >= 0.8:

            return "date"

    # =========================================
    # NUMERICAL
    # =========================================

    if pd.api.types.is_numeric_dtype(series):

        if len(non_null) == 0:

            return "numerical"

        unique_count = series.nunique()

        # Binary numerical column
        if unique_count <= 2:

            return "binary"

        # Low-cardinality integer values
        if (
            pd.api.types.is_integer_dtype(series)
            and unique_count <= 10
        ):

            return "categorical_numeric"

        return "numerical"

    # =========================================
    # TEXT / CATEGORICAL
    # =========================================

    unique_count = series.nunique()

    row_count = len(series)

    if row_count > 0:

        unique_ratio = unique_count / row_count

    else:

        unique_ratio = 0

    # High-cardinality text may represent
    # identifiers, names, emails, etc.

    if unique_ratio > 0.8:

        return "identifier_or_text"

    return "categorical"


def _detect_semantic_tags(column_name, series, role):
    """
    Generate broad semantic tags for a column.

    These tags help the query planner understand
    what a column may represent.
    """

    name = str(column_name).lower().strip()

    tags = []

    # =========================================
    # TIME
    # =========================================

    time_words = [
        "date",
        "time",
        "year",
        "month",
        "week",
        "day",
        "quarter"
    ]

    if any(
        word in name
        for word in time_words
    ):

        tags.append("time")

    # =========================================
    # IDENTITY
    # =========================================

    identity_words = [
        "id",
        "code",
        "number",
        "no",
        "name"
    ]

    if any(
        word in name
        for word in identity_words
    ):

        tags.append("identifier")

    # =========================================
    # LOCATION
    # =========================================

    location_words = [
        "country",
        "city",
        "state",
        "region",
        "location",
        "address",
        "area"
    ]

    if any(
        word in name
        for word in location_words
    ):

        tags.append("location")

    # =========================================
    # FINANCIAL / MONEY
    # =========================================

    financial_words = [
        "price",
        "cost",
        "revenue",
        "sales",
        "income",
        "profit",
        "salary",
        "amount",
        "rate",
        "adr",
        "fare",
        "expense"
    ]

    if any(
        word in name
        for word in financial_words
    ):

        tags.append("financial")

    # =========================================
    # STATUS
    # =========================================

    status_words = [
        "status",
        "state",
        "cancel",
        "canceled",
        "cancelled",
        "active",
        "approved",
        "completed",
        "success",
        "failure"
    ]

    if any(
        word in name
        for word in status_words
    ):

        tags.append("status")

    # =========================================
    # DEMOGRAPHICS
    # =========================================

    demographic_words = [
        "gender",
        "sex",
        "age",
        "education",
        "occupation",
        "department",
        "marital"
    ]

    if any(
        word in name
        for word in demographic_words
    ):

        tags.append("demographic")

    # =========================================
    # COUNT / QUANTITY
    # =========================================

    quantity_words = [
        "count",
        "quantity",
        "number",
        "total",
        "units",
        "orders",
        "bookings",
        "customers",
        "guests"
    ]

    if any(
        word in name
        for word in quantity_words
    ):

        tags.append("quantity")

    # =========================================
    # ROLE-BASED TAGS
    # =========================================

    if role == "numerical":

        tags.append("measure")

    elif role == "categorical":

        tags.append("dimension")

    elif role == "date":

        tags.append("time_dimension")

    elif role == "binary":

        tags.append("indicator")

    return list(dict.fromkeys(tags))


def analyze_schema(df):
    """
    Analyze the structure and general meaning of
    columns in any uploaded dataset.
    """

    schema = {
        "columns": [],
        "numerical_columns": [],
        "categorical_columns": [],
        "date_columns": [],
        "column_details": {}
    }

    for column in df.columns:

        column_name = str(column)

        series = df[column]

        # =========================================
        # BASIC INFORMATION
        # =========================================

        details = {
            "name": column_name,
            "dtype": str(series.dtype),
            "missing": int(
                series.isnull().sum()
            ),
            "unique": int(
                series.nunique()
            )
        }

        schema["columns"].append(
            column_name
        )

        # =========================================
        # DETECT ROLE
        # =========================================

        role = _detect_column_role(
            column_name,
            series
        )

        details["role"] = role

        # =========================================
        # SEMANTIC TAGS
        # =========================================

        details["semantic_tags"] = (
            _detect_semantic_tags(
                column_name,
                series,
                role
            )
        )

        # =========================================
        # COLUMN CATEGORIES
        # =========================================

        if role == "numerical":

            schema[
                "numerical_columns"
            ].append(column_name)

        elif role in [
            "categorical",
            "categorical_numeric",
            "binary"
        ]:

            schema[
                "categorical_columns"
            ].append(column_name)

        elif role == "date":

            schema[
                "date_columns"
            ].append(column_name)

        # =========================================
        # SAMPLE VALUES
        # =========================================

        sample_values = (
            series
            .dropna()
            .astype(str)
            .head(5)
            .tolist()
        )

        details["sample_values"] = (
            sample_values
        )

        # =========================================
        # STORE DETAILS
        # =========================================

        schema[
            "column_details"
        ][column_name] = details

    return schema