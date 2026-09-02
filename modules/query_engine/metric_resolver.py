import pandas as pd


def _is_numeric_column(
    column,
    schema,
    dataframe=None
):
    """
    Determine whether a column can be used as a
    numerical analytical measure.
    """

    if (
        dataframe is not None
        and column in dataframe.columns
    ):

        values = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

        if values.notna().any():
            return True

    column_details = schema.get(
        "column_details",
        {}
    )

    details = column_details.get(
        column,
        {}
    )

    role = details.get(
        "role"
    )

    return role in [
        "numerical",
        "numeric",
        "number",
        "integer",
        "float"
    ]


def _get_candidate_score(item):
    try:
        return float(
            item.get(
                "score",
                0
            )
        )
    except (
        TypeError,
        ValueError
    ):
        return 0.0


def _get_best_numeric_candidate(
    matched_columns,
    schema,
    dataframe=None
):
    """
    Find the most relevant numeric column.
    """

    candidates = []

    for item in matched_columns:

        column = item.get(
            "column"
        )

        if not column:
            continue

        if _is_numeric_column(
            column,
            schema,
            dataframe
        ):

            candidates.append(
                (
                    column,
                    _get_candidate_score(
                        item
                    )
                )
            )

    if not candidates:
        return None

    candidates.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return candidates[0][0]


def _get_best_binary_candidate(
    matched_columns,
    schema,
    dataframe=None,
    question=""
):
    """
    Find the most relevant binary indicator.

    Uses:
    - matched-column score
    - binary schema role
    - actual 0/1 values
    - semantic similarity with the user's question
    """

    column_details = schema.get(
        "column_details",
        {}
    )

    candidates = []

    question_text = str(
        question
    ).lower().replace("_", " ")

    # =========================================
    # CHECK MATCHED COLUMNS
    # =========================================

    for item in matched_columns:

        column = item.get(
            "column"
        )

        if not column:
            continue

        details = column_details.get(
            column,
            {}
        )

        role = details.get(
            "role"
        )

        column_text = str(
            column
        ).lower().replace("_", " ")

        score = _get_candidate_score(
            item
        )

        # -------------------------------------
        # Binary role
        # -------------------------------------

        is_binary = (
            role == "binary"
        )

        # -------------------------------------
        # Actual 0/1 detection
        # -------------------------------------

        if (
            not is_binary
            and dataframe is not None
            and column in dataframe.columns
        ):

            values = pd.to_numeric(
                dataframe[column],
                errors="coerce"
            ).dropna()

            if not values.empty:

                unique_values = set(
                    values.unique()
                )

                is_binary = (
                    unique_values.issubset(
                        {0, 1}
                    )
                )

        if not is_binary:
            continue

        # -------------------------------------
        # Semantic relevance
        # -------------------------------------

        semantic_score = 0

        column_words = set(
            column_text.split()
        )

        question_words = set(
            question_text.split()
        )

        semantic_score += len(
            column_words & question_words
        ) * 5

        # -------------------------------------
        # Common indicator naming patterns
        # -------------------------------------

        indicator_words = [
            "cancel",
            "canceled",
            "cancelled",
            "churn",
            "active",
            "approved",
            "success",
            "failed",
            "default",
            "converted",
            "response",
            "returned",
            "repeated",
            "fraud",
            "yes",
            "no"
        ]

        for word in indicator_words:

            if (
                word in question_text
                and word in column_text
            ):
                semantic_score += 8

        final_score = (
            score
            + semantic_score
        )

        candidates.append(
            (
                column,
                final_score
            )
        )

    # =========================================
    # RETURN BEST MATCH
    # =========================================

    if not candidates:
        return None

    candidates.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return candidates[0][0]


def resolve_metric(
    question,
    matched_columns,
    schema,
    parsed_query=None,
    dataframe=None
):
    """
    Resolve the analytical operation and measure
    requested by the user.

    Dataset-independent.
    """

    original_question = (
        question
        .lower()
        .strip()
    )

    metric = {
        "type": "count",
        "column": None,
        "group_by": None,
        "confidence": 0.0
    }

    # =========================================
    # CANDIDATES
    # =========================================

    candidates = [
        item.get("column")
        for item in matched_columns
        if item.get("column")
    ]

    # =========================================
    # PARSER OPERATION
    # =========================================

    parsed_operation = None

    if parsed_query:

        parsed_operation = (
            parsed_query.get(
                "statistical_operation"
            )
        )

    # =========================================
    # DETECT OPERATION
    # =========================================

    # -----------------------------------------
    # COUNT
    # -----------------------------------------

    count_phrases = [
        "how many",
        "how much records",
        "number of records",
        "number of rows",
        "count of records",
        "count records",
        "count rows",
        "total records",
        "total rows"
    ]

    # -----------------------------------------
    # SUM
    # -----------------------------------------

    sum_phrases = [
        "sum",
        "total amount",
        "total sales",
        "total revenue",
        "total cost",
        "overall amount",
        "overall total",
        "total value",
        "total"
    ]

    # -----------------------------------------
    # MEAN
    # -----------------------------------------

    mean_phrases = [
        "average",
        "avg",
        "mean",
        "on average"
    ]

    # -----------------------------------------
    # MEDIAN
    # -----------------------------------------

    median_phrases = [
        "median",
        "middle value"
    ]

    # -----------------------------------------
    # MIN
    # -----------------------------------------

    min_phrases = [
        "minimum",
        "min value",
        "lowest",
        "smallest",
        "least"
    ]

    # -----------------------------------------
    # MAX
    # -----------------------------------------

    max_phrases = [
        "maximum",
        "max value",
        "highest",
        "largest",
        "greatest",
        "most"
    ]

    # -----------------------------------------
    # RATE
    # -----------------------------------------

    rate_phrases = [
        "rate",
        "percentage",
        "percent",
        "%",
        "ratio",
        "proportion",
        "share"
    ]

    # -----------------------------------------
    # DISTRIBUTION
    # -----------------------------------------

    distribution_phrases = [
        "distribution",
        "spread",
        "frequency",
        "breakdown",
        "how often"
    ]

    # =========================================
    # PRIORITY
    # =========================================

    # Explicit parser result gets priority.

    if parsed_operation == "mean":

        metric["type"] = "mean"
        metric["confidence"] = 0.9

    elif parsed_operation == "median":

        metric["type"] = "median"
        metric["confidence"] = 0.9

    elif parsed_operation == "min":

        metric["type"] = "min"
        metric["confidence"] = 0.85

    elif parsed_operation == "max":

        metric["type"] = "max"
        metric["confidence"] = 0.85

    elif parsed_operation == "sum":

        metric["type"] = "sum"
        metric["confidence"] = 0.9

    else:

        # =====================================
        # RATE
        # =====================================

        if any(
            phrase in original_question
            for phrase in rate_phrases
        ):

            metric["type"] = "rate"
            metric["confidence"] = 0.9

        # =====================================
        # MEAN
        # =====================================

        elif any(
            phrase in original_question
            for phrase in mean_phrases
        ):

            metric["type"] = "mean"
            metric["confidence"] = 0.9

        # =====================================
        # MEDIAN
        # =====================================

        elif any(
            phrase in original_question
            for phrase in median_phrases
        ):

            metric["type"] = "median"
            metric["confidence"] = 0.9

        # =====================================
        # MAX
        # =====================================

        elif any(
            phrase in original_question
            for phrase in max_phrases
        ):

            metric["type"] = "max"
            metric["confidence"] = 0.85

        # =====================================
        # MIN
        # =====================================

        elif any(
            phrase in original_question
            for phrase in min_phrases
        ):

            metric["type"] = "min"
            metric["confidence"] = 0.85

        # =====================================
        # DISTRIBUTION
        # =====================================

        elif any(
            phrase in original_question
            for phrase in distribution_phrases
        ):

            metric["type"] = "distribution"
            metric["confidence"] = 0.85

        # =====================================
        # SUM
        # =====================================

        elif any(
            phrase in original_question
            for phrase in sum_phrases
        ):

            # Important:
            #
            # "total records"
            # "total rows"
            #
            # are COUNT, not SUM.

            if any(
                phrase in original_question
                for phrase in count_phrases
            ):

                metric["type"] = "count"
                metric["confidence"] = 0.8

            else:

                metric["type"] = "sum"
                metric["confidence"] = 0.9

        # =====================================
        # COUNT
        # =====================================

        elif any(
            phrase in original_question
            for phrase in count_phrases
        ):

            metric["type"] = "count"
            metric["confidence"] = 0.8

    # =========================================
    # NUMERICAL METRICS
    # =========================================

    numerical_metrics = [
        "mean",
        "median",
        "min",
        "max",
        "sum",
        "distribution"
    ]

    if metric["type"] in numerical_metrics:

        best_numeric = (
            _get_best_numeric_candidate(
                matched_columns,
                schema,
                dataframe
            )
        )

        if best_numeric:

            metric["column"] = (
                best_numeric
            )

        else:

            # Explicit requested measure fallback

            requested_measure = None

            if parsed_query:

                requested_measure = (
                    parsed_query.get(
                        "requested_measure_text"
                    )
                )

            if requested_measure:

                normalized_requested = (
                    str(
                        requested_measure
                    )
                    .lower()
                    .strip()
                )

                if dataframe is not None:

                    for column in (
                        dataframe.columns
                    ):

                        normalized_column = (
                            str(column)
                            .lower()
                            .strip()
                        )

                        if (
                            normalized_column
                            == normalized_requested
                        ):

                            if _is_numeric_column(
                                column,
                                schema,
                                dataframe
                            ):

                                metric["column"] = (
                                    column
                                )

                                break

    # =========================================
    # RATE
    # =========================================

        # =========================================
    # RATE
    # =========================================

    if metric["type"] == "rate":

        best_binary = (
            _get_best_binary_candidate(
                matched_columns,
                schema,
                dataframe,
                question
            )
        )

        if best_binary:

            metric["column"] = best_binary

        elif dataframe is not None:

            binary_candidates = []

            question_text = (
                original_question
                .replace("_", " ")
            )

            for column in dataframe.columns:

                values = pd.to_numeric(
                    dataframe[column],
                    errors="coerce"
                ).dropna()

                if values.empty:
                    continue

                unique_values = set(
                    values.unique()
                )

                if not unique_values.issubset({0, 1}):
                    continue

                column_text = (
                    str(column)
                    .lower()
                    .replace("_", " ")
                )

                score = 0

                # Direct word similarity
                for word in column_text.split():

                    if word in question_text:
                        score += 5

                # Semantic indicator matching
                indicator_terms = [
                    "cancel",
                    "canceled",
                    "cancelled",
                    "churn",
                    "active",
                    "approved",
                    "success",
                    "failed",
                    "default",
                    "converted",
                    "returned",
                    "repeated",
                    "fraud"
                ]

                for term in indicator_terms:

                    if term in question_text:

                        if (
                            term[:5]
                            in column_text
                        ):
                            score += 10

                binary_candidates.append(
                    (
                        column,
                        score
                    )
                )

            if binary_candidates:

                binary_candidates.sort(
                    key=lambda item: item[1],
                    reverse=True
                )

                metric["column"] = (
                    binary_candidates[0][0]
                )

        # Final fallback
        if not metric["column"]:

            best_numeric = (
                _get_best_numeric_candidate(
                    matched_columns,
                    schema,
                    dataframe
                )
            )

            if best_numeric:

                values = pd.to_numeric(
                    dataframe[best_numeric],
                    errors="coerce"
                ).dropna()

                if (
                    not values.empty
                    and set(
                        values.unique()
                    ).issubset({0, 1})
                ):

                    metric["column"] = (
                        best_numeric
                    )    

    # =========================================
    # COUNT
    # =========================================

    if metric["type"] == "count":

        if candidates:

            metric["column"] = (
                candidates[0]
            )

    return metric