import re


def normalize_text(text):
    """
    Normalize text so column names and user language
    can be compared more easily.
    """

    text = str(text).lower().strip()

    text = text.replace("_", " ")
    text = text.replace("-", " ")

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def get_column_tokens(column_name):
    """
    Convert a column name into searchable words.
    """

    normalized = normalize_text(
        column_name
    )

    return set(
        normalized.split()
    )


def _text_tokens(text):
    """
    Return normalized searchable tokens.
    """

    normalized = normalize_text(
        text
    )

    if not normalized:
        return set()

    return set(
        normalized.split()
    )


def _token_similarity(
    requested_text,
    column_name
):
    """
    Calculate similarity between explicitly requested
    measure/group text and a dataset column.

    This is dataset-independent.

    Examples:

        requested = "adr"
        column = "adr"

        requested = "customer salary"
        column = "salary"

        requested = "booking status"
        column = "booking_status"
    """

    if not requested_text:
        return 0.0

    requested = normalize_text(
        requested_text
    )

    column = normalize_text(
        column_name
    )

    if not requested or not column:
        return 0.0

    score = 0.0

    # =========================================
    # EXACT MATCH
    # =========================================

    if requested == column:

        score += 30

        return score


    # =========================================
    # REQUESTED TEXT IS EXACT COLUMN NAME
    # =========================================

    if column in requested:

        score += 25


    # =========================================
    # COLUMN NAME APPEARS IN REQUEST
    # =========================================

    if requested in column:

        score += 25


    requested_tokens = set(
        requested.split()
    )

    column_tokens = set(
        column.split()
    )


    # =========================================
    # TOKEN MATCH
    # =========================================

    matching_tokens = (
        requested_tokens
        & column_tokens
    )

    score += (
        len(matching_tokens) * 8
    )


    # =========================================
    # ALL COLUMN TOKENS MATCH
    # =========================================

    if (
        column_tokens
        and column_tokens.issubset(
            requested_tokens
        )
    ):

        score += 12


    return score


def score_column_match(
    column_name,
    question,
    details=None,
    parsed_query=None
):
    """
    Calculate how strongly a dataset column relates
    to the user's question.

    Uses:

    - exact column names
    - column-name words
    - explicitly requested measure
    - explicitly requested grouping
    - semantic tags
    - sample values
    """

    question_text = normalize_text(
        question
    )

    question_words = set(
        question_text.split()
    )

    column_text = normalize_text(
        column_name
    )

    column_words = get_column_tokens(
        column_name
    )

    score = 0.0


    # =========================================
    # DIRECT COLUMN NAME MATCH
    # =========================================

    if column_text in question_text:

        score += 10


    # =========================================
    # WORD MATCH
    # =========================================

    matching_words = (
        column_words
        & question_words
    )

    score += (
        len(matching_words) * 3
    )


    # =========================================
    # PARSED REQUEST
    # =========================================

    if parsed_query:

        requested_measure = (
            parsed_query.get(
                "requested_measure_text"
            )
        )

        grouping_text = (
            parsed_query.get(
                "grouping_text"
            )
        )


        # -------------------------------------
        # REQUESTED MEASURE
        # -------------------------------------

        measure_score = (
            _token_similarity(
                requested_measure,
                column_name
            )
        )

        score += measure_score


        # -------------------------------------
        # REQUESTED GROUPING
        # -------------------------------------

        grouping_score = (
            _token_similarity(
                grouping_text,
                column_name
            )
        )

        # Grouping is important, but slightly
        # weaker than the requested measure.

        score += (
            grouping_score * 0.8
        )


    # =========================================
    # SEMANTIC TAGS
    # =========================================

    if details:

        tags = details.get(
            "semantic_tags",
            []
        )

        for tag in tags:

            tag_words = set(
                normalize_text(tag).split()
            )

            if tag_words & question_words:

                score += 2


    # =========================================
    # SAMPLE VALUE MATCH
    # =========================================

    if details:

        sample_values = details.get(
            "sample_values",
            []
        )

        for value in sample_values:

            value_text = normalize_text(
                value
            )

            if (
                value_text
                and value_text in question_text
            ):

                score += 1


    return score


def match_columns(
    df,
    schema,
    question,
    parsed_query=None,
    max_columns=5
):
    """
    Find the most relevant dataset columns
    for a natural-language question.

    Returns a ranked list of columns.

    The matcher remains dataset-independent.
    """

    matches = []

    column_details = schema.get(
        "column_details",
        {}
    )


    for column in df.columns:

        column_name = str(column)

        details = column_details.get(
            column_name,
            {}
        )


        score = score_column_match(
            column_name,
            question,
            details,
            parsed_query
        )


        matches.append({

            "column": column_name,

            "score": round(
                score,
                2
            ),

            "role": details.get(
                "role"
            ),

            "semantic_tags": details.get(
                "semantic_tags",
                []
            )
        })


    # =========================================
    # SORT
    # =========================================

    matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )


    # =========================================
    # REMOVE ZERO-SCORE COLUMNS
    # =========================================

    useful_matches = [
        item
        for item in matches
        if item["score"] > 0
    ]


    return useful_matches[
        :max_columns
    ]