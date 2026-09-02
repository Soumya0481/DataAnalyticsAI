import re


def parse_query(question):
    """
    Analyze a user's natural-language analytical request.

    This function does not calculate anything.
    It creates a structured description of what
    the user is asking for.

    The parser is dataset-independent.
    """

    original_question = (
        question.strip()
        if question
        else ""
    )

    question_lower = (
        original_question.lower()
    )

    result = {
        "question": original_question,
        "intent": "analysis",

        "wants_visualization": False,
        "wants_comparison": False,
        "wants_summary": False,
        "wants_trend": False,
        "wants_ranking": False,
        "wants_percentage": False,
        "wants_distribution": False,
        "wants_relationship": False,
        "wants_statistics": False,

        "requested_chart": None,

        # NEW:
        # Indicates whether the user explicitly
        # requested grouping/comparison.
        "wants_grouping": False,

        # NEW:
        # Textual grouping phrase extracted from
        # the question when possible.
        "grouping_text": None,

        # NEW:
        # The phrase after analytical keywords.
        # Example:
        # "average ADR"
        # -> "ADR"
        "requested_measure_text": None,

        # NEW:
        # Statistical operation requested.
        "statistical_operation": None,
    }

    # =========================================
    # EMPTY QUESTION
    # =========================================

    if not question_lower:

        result["intent"] = "unknown"

        return result


    # =========================================
    # SUMMARY / OVERVIEW
    # =========================================

    summary_terms = [
        "summary",
        "summarize",
        "overview",
        "describe",
        "overall",
        "give me an overview",
        "tell me about the data",
        "tell me about my data",
        "what can you tell me",
        "dataset summary",
        "data summary"
    ]

    if any(
        term in question_lower
        for term in summary_terms
    ):

        result["intent"] = "summary"

        result["wants_summary"] = True


    # =========================================
    # VISUALIZATION
    # =========================================

    visualization_terms = [
        "graph",
        "chart",
        "plot",
        "visualization",
        "visualize",
        "visual",
        "display",
        "show me",
        "draw",
        "visualise",
        "visualisation"
    ]

    if any(
        term in question_lower
        for term in visualization_terms
    ):

        result["wants_visualization"] = True


    # =========================================
    # EXPLICIT CHART TYPE
    # =========================================

    if (
        "bar chart" in question_lower
        or "bar graph" in question_lower
        or "bar plot" in question_lower
    ):

        result["requested_chart"] = "bar"

        result["wants_visualization"] = True


    elif (
        "line chart" in question_lower
        or "line graph" in question_lower
        or "line plot" in question_lower
    ):

        result["requested_chart"] = "line"

        result["wants_visualization"] = True


    elif (
        "pie chart" in question_lower
        or "pie graph" in question_lower
        or "pie plot" in question_lower
    ):

        result["requested_chart"] = "pie"

        result["wants_visualization"] = True


    elif (
        "scatter plot" in question_lower
        or "scatter chart" in question_lower
        or "scatter graph" in question_lower
    ):

        result["requested_chart"] = "scatter"

        result["wants_visualization"] = True


    elif (
        "histogram" in question_lower
        or "histogram chart" in question_lower
        or "histogram plot" in question_lower
    ):

        result["requested_chart"] = "histogram"

        result["wants_visualization"] = True


    # =========================================
    # COMPARISON
    # =========================================

    comparison_terms = [
        "compare",
        "comparison",
        "compare between",
        "compare with",
        "compared with",
        "versus",
        "vs",
        "against",
        "difference between",
        "difference in",
        "which is better",
        "which one is higher",
        "which one is lower",
        "compare the"
    ]

    if any(
        term in question_lower
        for term in comparison_terms
    ):

        result["intent"] = "comparison"

        result["wants_comparison"] = True


    # =========================================
    # GROUPING
    # =========================================
    #
    # Examples:
    #
    # cancellation rate BY hotel
    # average price PER category
    # revenue FOR EACH region
    #
    # =========================================

    grouping_patterns = [
        r"\bby\s+(.+)",
        r"\bper\s+(.+)",
        r"\bfor each\s+(.+)",
        r"\bfor every\s+(.+)",
        r"\bamong\s+(.+)"
    ]

    for pattern in grouping_patterns:

        match = re.search(
            pattern,
            question_lower
        )

        if match:

            grouping_text = (
                match.group(1)
                .strip()
            )

            # Remove common trailing words.
            grouping_text = re.sub(
                r"\b(chart|graph|plot|visualization)\b.*$",
                "",
                grouping_text
            ).strip()

            if grouping_text:

                result["wants_grouping"] = True

                result["grouping_text"] = (
                    grouping_text
                )

                break


    # =========================================
    # TREND / TIME ANALYSIS
    # =========================================

    trend_terms = [
        "trend",
        "over time",
        "with time",
        "change over time",
        "growth over time",
        "monthly trend",
        "weekly trend",
        "daily trend",
        "yearly trend",
        "month by month",
        "week by week",
        "day by day",
        "year by year",
        "over the years",
        "over months",
        "over weeks",
        "over days"
    ]

    if any(
        term in question_lower
        for term in trend_terms
    ):

        result["intent"] = "trend"

        result["wants_trend"] = True


    # =========================================
    # RANKING
    # =========================================

    ranking_terms = [
        "top",
        "bottom",
        "highest",
        "lowest",
        "largest",
        "smallest",
        "best",
        "worst",
        "most",
        "least",
        "rank",
        "ranking",
        "leading",
        "performing best"
    ]

    if any(
        term in question_lower
        for term in ranking_terms
    ):

        result["intent"] = "ranking"

        result["wants_ranking"] = True


    # =========================================
    # PERCENTAGE / RATE
    # =========================================

    percentage_terms = [
        "percentage",
        "percent",
        "%",
        "rate",
        "ratio",
        "proportion",
        "share",
        "contribution"
    ]

    if any(
        term in question_lower
        for term in percentage_terms
    ):

        result["wants_percentage"] = True


    # =========================================
    # DISTRIBUTION
    # =========================================

    distribution_terms = [
        "distribution",
        "spread",
        "frequency",
        "how often",
        "breakdown",
        "break down",
        "distribution of",
        "frequency of"
    ]

    if any(
        term in question_lower
        for term in distribution_terms
    ):

        result["wants_distribution"] = True


    # =========================================
    # RELATIONSHIP / CORRELATION
    # =========================================

    relationship_terms = [
        "relationship",
        "correlation",
        "related",
        "relationship between",
        "correlated",
        "association",
        "connected",
        "relationship of",
        "scatter plot",
        "scatter chart",
        "scatter graph"
    ]

    if any(
        term in question_lower
        for term in relationship_terms
    ):

        result["intent"] = "relationship"

        result["wants_relationship"] = True


    # =========================================
    # STATISTICAL OPERATION
    # =========================================

    # IMPORTANT:
    #
    # We explicitly identify the operation,
    # but we do NOT identify a dataset column
    # here.
    #
    # The column matcher will do that later.

    statistical_operations = {

        "mean": [
            "average",
            "mean",
            "avg"
        ],

        "median": [
            "median"
        ],

        "min": [
            "minimum",
            "minimum value",
            "min value",
            "min"
        ],

        "max": [
            "maximum",
            "maximum value",
            "max value",
            "max"
        ],

        "std": [
            "standard deviation",
            "std deviation",
            "std"
        ],

        "variance": [
            "variance",
            "var"
        ]
    }


    for operation, terms in (
        statistical_operations.items()
    ):

        if any(
            term in question_lower
            for term in terms
        ):

            result["wants_statistics"] = True

            result["statistical_operation"] = (
                operation
            )

            break


    # =========================================
    # EXTRACT REQUESTED MEASURE TEXT
    # =========================================
    #
    # Examples:
    #
    # What is the average ADR?
    #                    ↑
    #
    # What is the average salary?
    #                         ↑
    #
    # Show maximum revenue
    #               ↑
    #
    # The parser doesn't decide whether the
    # text is a real column. The matcher does.
    #
    # =========================================

    operation_words = (
        "average|mean|avg|"
        "median|"
        "minimum|minimum value|min value|min|"
        "maximum|maximum value|max value|max|"
        "standard deviation|std deviation|std|"
        "variance|var"
    )

    measure_patterns = [

        rf"\b(?:what\s+is\s+)?(?:the\s+)?"
        rf"(?:{operation_words})\s+of\s+(.+?)(?:\?|$)",

        rf"\b(?:what\s+is\s+)?(?:the\s+)?"
        rf"(?:{operation_words})\s+(.+?)(?:\?|$)",

        rf"\b(?:calculate|find|show|get)\s+"
        rf"(?:the\s+)?"
        rf"(?:{operation_words})\s+of\s+(.+?)(?:\?|$)",

        rf"\b(?:calculate|find|show|get)\s+"
        rf"(?:the\s+)?"
        rf"(?:{operation_words})\s+(.+?)(?:\?|$)"
    ]


    if result["wants_statistics"]:

        for pattern in measure_patterns:

            match = re.search(
                pattern,
                question_lower
            )

            if match:

                measure_text = (
                    match.group(1)
                    .strip()
                )

                # Remove grouping phrase.
                measure_text = re.split(
                    r"\s+\bby\b\s+",
                    measure_text,
                    maxsplit=1
                )[0]

                measure_text = re.split(
                    r"\s+\bper\b\s+",
                    measure_text,
                    maxsplit=1
                )[0]

                measure_text = (
                    measure_text
                    .strip(" ?.,")
                )

                if measure_text:

                    result[
                        "requested_measure_text"
                    ] = measure_text

                    break


    # =========================================
    # FALLBACK MEASURE EXTRACTION
    # =========================================

    if (
        result["wants_statistics"]
        and not result[
            "requested_measure_text"
        ]
    ):

        # Remove common analytical language
        # and keep the likely column phrase.

        cleaned = question_lower

        remove_terms = [
            "what is",
            "what's",
            "calculate",
            "find",
            "show me",
            "show",
            "give me",
            "tell me",
            "the",
            "average",
            "mean",
            "avg",
            "median",
            "minimum",
            "minimum value",
            "min value",
            "maximum",
            "maximum value",
            "max value",
            "standard deviation",
            "std deviation",
            "std",
            "variance",
            "var",
            "please",
            "of"
        ]

        for term in remove_terms:

            cleaned = re.sub(
                rf"\b{re.escape(term)}\b",
                " ",
                cleaned
            )

        # Remove grouping section.
        cleaned = re.split(
            r"\s+\bby\b\s+",
            cleaned,
            maxsplit=1
        )[0]

        cleaned = re.split(
            r"\s+\bper\b\s+",
            cleaned,
            maxsplit=1
        )[0]

        cleaned = re.sub(
            r"\s+",
            " ",
            cleaned
        ).strip(
            " ?.,"
        )

        if cleaned:

            result[
                "requested_measure_text"
            ] = cleaned


    # =========================================
    # VISUAL ANALYSIS
    # =========================================

    if (
        result["wants_visualization"]
        and result["intent"] == "analysis"
    ):

        result["intent"] = (
            "visual_analysis"
        )


    # =========================================
    # GENERAL STATISTICS
    # =========================================

    if (
        result["intent"] == "analysis"
        and result["wants_statistics"]
    ):

        result["intent"] = "statistics"


    # =========================================
    # GROUPED STATISTICS
    # =========================================

    if (
        result["wants_grouping"]
        and result["wants_statistics"]
        and result["intent"]
        == "statistics"
    ):

        result["intent"] = (
            "comparison"
        )

        result["wants_comparison"] = True


    return result