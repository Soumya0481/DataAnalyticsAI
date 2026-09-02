def select_chart(
    result_data,
    parsed_query,
    plan
):
    """
    Decide whether a chart is appropriate and
    select a suitable chart type.

    Returns:
        None
        "bar"
        "line"
        "pie"
        "scatter"
        "histogram"
    """

    if result_data is None:
        return None

    if result_data.empty:
        return None

    # =========================================
    # USER DID NOT REQUEST VISUALIZATION
    # =========================================

    if not parsed_query.get(
        "wants_visualization",
        False
    ):
        return None

    # =========================================
    # TREND
    # =========================================

    if parsed_query.get(
        "wants_trend",
        False
    ):

        return "line"

    # =========================================
    # COMPARISON
    # =========================================

    if parsed_query.get(
        "wants_comparison",
        False
    ):

        return "bar"

    # =========================================
    # RANKING
    # =========================================

    if parsed_query.get(
        "wants_ranking",
        False
    ):

        return "bar"
        # =========================================
    # EXPLICIT USER CHART REQUEST
    # =========================================

    requested_chart = parsed_query.get(
        "requested_chart"
    )

    if requested_chart:

        return requested_chart
    # =========================================
    # PERCENTAGE / COMPOSITION
    # =========================================

    if parsed_query.get(
        "wants_percentage",
        False
    ):

        # Pie charts work best when there
        # are only a reasonable number of categories.

        if len(result_data) <= 8:

            return "pie"

        return "bar"

    # =========================================
    # PLAN-SPECIFIC VISUALIZATION
    # =========================================

    planned_chart = plan.get(
        "visualization"
    )

    if planned_chart is not None:

        return planned_chart

    # =========================================
    # AUTOMATIC FALLBACK
    # =========================================

    numeric_columns = (
        result_data
        .select_dtypes(include="number")
        .columns
        .tolist()
    )

    categorical_columns = (
        result_data
        .select_dtypes(
            include=["object", "category", "bool"]
        )
        .columns
        .tolist()
    )

    # One numerical column → distribution
    if len(numeric_columns) == 1:

        if len(result_data) > 10:

            return "histogram"

        return "bar"

    # Category + numerical value → bar
    if (
        categorical_columns
        and numeric_columns
    ):

        return "bar"

    return None