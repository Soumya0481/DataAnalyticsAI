import pandas as pd


def _is_numeric_column(column, schema):
    """
    Determine whether a column is numerically usable.

    The planner should not blindly trust the inferred schema role.
    """

    column_details = schema.get(
        "column_details",
        {}
    )

    details = column_details.get(
        column,
        {}
    )

    # Schema role
    role = details.get("role")

    if role in [
        "numerical",
        "numeric",
        "number",
        "integer",
        "float"
    ]:
        return True

    # If schema stores dtype information
    dtype = str(
        details.get(
            "dtype",
            ""
        )
    ).lower()

    if any(
        value in dtype
        for value in [
            "int",
            "float",
            "double",
            "number"
        ]
    ):
        return True

    return False


def create_analysis_plan(
    schema,
    parsed_query,
    matched_columns,
    metric
):
    """
    Create a dataset-independent analytical plan.

    The resolved metric is treated as authoritative.
    The planner does not require a column to have a
    specific inferred schema role when that column has
    already been selected as the requested measure.
    """

    question = (
        parsed_query.get(
            "question",
            ""
        )
        .lower()
        .strip()
    )

    plan = {
        "intent": parsed_query.get(
            "intent",
            "analysis"
        ),
        "columns": [],
        "operations": [],
        "visualization": None,
        "group_by": None,
        "measure": metric.get(
            "column"
        ),
        "metric": metric,
        "status": "ready"
    }

    # =========================================
    # MATCHED COLUMNS
    # =========================================

    matched = [
        item.get("column")
        for item in matched_columns
        if item.get("column")
    ]

    column_details = schema.get(
        "column_details",
        {}
    )

    # =========================================
    # NUMERICAL COLUMNS
    # =========================================

    numerical_columns = [
        column
        for column in matched
        if _is_numeric_column(
            column,
            schema
        )
    ]

    # =========================================
    # CATEGORICAL COLUMNS
    # =========================================

    categorical_columns = [
        column
        for column in matched
        if column_details.get(
            column,
            {}
        ).get("role") in [
            "categorical",
            "categorical_numeric",
            "binary"
        ]
    ]

    # Fallback to schema-level categorical columns
    # when the grouping column is not among the
    # top matched columns.
    if not categorical_columns:

        categorical_columns = schema.get(
            "categorical_columns",
            []
        )

    # =========================================
    # DATE COLUMNS
    # =========================================

    date_columns = [
        column
        for column in matched
        if column_details.get(
            column,
            {}
        ).get("role") == "date"
    ]

    metric_type = metric.get(
        "type",
        "count"
    )

    metric_column = metric.get(
        "column"
    )

    # =========================================
    # GROUPING DETECTION
    # =========================================

    grouping_phrases = [
        " by ",
        " per ",
        " for each ",
        " for every ",
        " among "
    ]

    wants_grouping = any(
        phrase in f" {question} "
        for phrase in grouping_phrases
    )

    # =========================================
    # SUMMARY
    # =========================================

    if parsed_query.get(
        "wants_summary"
    ):

        plan["operations"].append(
            "dataset_summary"
        )

        return plan

        # =========================================
    # RELATIONSHIP
    # =========================================

    if parsed_query.get(
        "wants_relationship"
    ):

        all_numeric = schema.get(
            "numerical_columns",
            []
        )

        # If schema information is unreliable,
        # fall back to matched numeric columns.
        if len(all_numeric) < 2:

            all_numeric = numerical_columns

        if len(all_numeric) < 2:

            plan["status"] = (
                "At least two numerical "
                "columns are required for "
                "relationship analysis."
            )

            return plan

        # Use matched numerical columns
        # when the user explicitly mentions them.
        matched_numeric = [
            column
            for column in matched
            if _is_numeric_column(
                column,
                schema
            )
        ]

        if len(matched_numeric) >= 2:

            selected_numeric = matched_numeric[:2]

        else:

            selected_numeric = all_numeric[:2]

        plan["columns"] = selected_numeric

        plan["operations"].append(
            "correlation"
        )

        plan["visualization"] = "scatter"

        return plan

    # =========================================
    # TREND
    # =========================================

    if parsed_query.get(
        "wants_trend"
    ):

        if date_columns:

            plan["group_by"] = (
                date_columns[0]
            )

        elif categorical_columns:

            plan["group_by"] = (
                categorical_columns[0]
            )

        else:

            plan["status"] = (
                "No suitable time or "
                "category column was found."
            )

            return plan

        if metric_column:

            plan["measure"] = (
                metric_column
            )

            plan["columns"] = [
                plan["group_by"],
                metric_column
            ]

        elif numerical_columns:

            plan["measure"] = (
                numerical_columns[0]
            )

            plan["columns"] = [
                plan["group_by"],
                plan["measure"]
            ]

        else:

            plan["columns"] = [
                plan["group_by"]
            ]

        plan["operations"].append(
            "trend"
        )

        plan["visualization"] = "line"

        return plan

    # =========================================
    # RATE
    # =========================================

    if metric_type == "rate":

        if not metric_column:

            plan["status"] = (
                "No suitable indicator column "
                "was found for rate calculation."
            )

            return plan

        plan["measure"] = metric_column

        plan["columns"] = [
            metric_column
        ]

        if (
            wants_grouping
            and categorical_columns
        ):

            plan["group_by"] = (
                categorical_columns[0]
            )

            plan["columns"].insert(
                0,
                plan["group_by"]
            )

            plan["visualization"] = "bar"

        plan["operations"].append(
            "percentage_by_indicator"
        )

        return plan

    # =========================================
    # NUMERICAL STATISTICS
    # =========================================

    if metric_type in [
        "mean",
        "median",
        "min",
        "max",
        "sum",
        "std",
        "variance",
        "distribution"
    ]:

        # =====================================
        # MOST IMPORTANT RULE:
        #
        # If metric resolver already selected
        # a measure, TRUST IT.
        # =====================================

        if metric_column:

            plan["measure"] = (
                metric_column
            )

        elif numerical_columns:

            plan["measure"] = (
                numerical_columns[0]
            )

        else:

            plan["status"] = (
                "No numerical measure "
                "was found for this analysis."
            )

            return plan

        plan["columns"] = [
            plan["measure"]
        ]

        # =====================================
        # GROUPED NUMERICAL ANALYSIS
        # =====================================

        if (
            wants_grouping
            and categorical_columns
        ):

            plan["group_by"] = (
                categorical_columns[0]
            )

            plan["columns"].insert(
                0,
                plan["group_by"]
            )

            if metric_type == "mean":

                plan["operations"].append(
                    "compare"
                )

            elif metric_type == "sum":

                plan["operations"].append(
                    "sum_by_category"
                )

            elif metric_type == "distribution":

                plan["operations"].append(
                    "distribution"
                )

            else:

                plan["operations"].append(
                    metric_type
                )

            plan["visualization"] = "bar"

            return plan

        # =====================================
        # SINGLE-COLUMN STATISTICS
        # =====================================

        if metric_type == "mean":

            plan["operations"].append(
                "statistical_analysis"
            )

        elif metric_type == "median":

            plan["operations"].append(
                "median"
            )

        elif metric_type == "min":

            plan["operations"].append(
                "min"
            )

        elif metric_type == "max":

            plan["operations"].append(
                "max"
            )

        elif metric_type == "sum":

            plan["operations"].append(
                "sum"
            )

        elif metric_type == "std":

            plan["operations"].append(
                "statistical_analysis"
            )

        elif metric_type == "variance":

            plan["operations"].append(
                "statistical_analysis"
            )

        elif metric_type == "distribution":

            plan["operations"].append(
                "distribution"
            )

            plan["visualization"] = (
                "histogram"
            )

        return plan

        # =========================================
    # COUNT
    # =========================================

    if metric_type == "count":

        if metric_column:

            plan["measure"] = metric_column

            plan["columns"] = [
                metric_column
            ]

        # Handle grouped count queries
        if wants_grouping and categorical_columns:

            plan["group_by"] = categorical_columns[0]

            plan["operations"].append(
                "categorical_distribution"
            )

            plan["visualization"] = (
                parsed_query.get("requested_chart")
                or "bar"
            )

            return plan

        plan["operations"].append(
            "count"
        )

        return plan

    # =========================================
    # COMPARISON
    # =========================================

    if parsed_query.get(
        "wants_comparison"
    ):

        if categorical_columns:

            plan["group_by"] = (
                categorical_columns[0]
            )

        if metric_column:

            plan["measure"] = (
                metric_column
            )

        elif numerical_columns:

            plan["measure"] = (
                numerical_columns[0]
            )

        if plan["group_by"]:

            plan["columns"] = [
                plan["group_by"]
            ]

        if plan["measure"]:

            plan["columns"].append(
                plan["measure"]
            )

            plan["operations"].append(
                "compare"
            )

            plan["visualization"] = "bar"

        elif plan["group_by"]:

            plan["operations"].append(
                "categorical_distribution"
            )

            plan["visualization"] = "bar"

        else:

            plan["status"] = (
                "No suitable columns were "
                "found for comparison."
            )

        return plan

    # =========================================
    # RANKING
    # =========================================

    if parsed_query.get(
        "wants_ranking"
    ):

        if not categorical_columns:

            plan["status"] = (
                "No category was found "
                "for ranking."
            )

            return plan

        plan["group_by"] = (
            categorical_columns[0]
        )

        if metric_column:

            plan["measure"] = (
                metric_column
            )

        elif numerical_columns:

            plan["measure"] = (
                numerical_columns[0]
            )

        else:

            plan["status"] = (
                "No numerical measure "
                "was found for ranking."
            )

            return plan

        plan["columns"] = [
            plan["group_by"],
            plan["measure"]
        ]

        plan["operations"].append(
            "ranking"
        )

        plan["visualization"] = "bar"

        return plan

    # =========================================
    # VISUALIZATION
    # =========================================

    if parsed_query.get(
        "wants_visualization"
    ):

        if (
            categorical_columns
            and numerical_columns
        ):

            plan["group_by"] = (
                categorical_columns[0]
            )

            plan["measure"] = (
                numerical_columns[0]
            )

            plan["columns"] = [
                plan["group_by"],
                plan["measure"]
            ]

            plan["operations"].append(
                "compare"
            )

            plan["visualization"] = "bar"

            return plan

        if numerical_columns:

            plan["measure"] = (
                numerical_columns[0]
            )

            plan["columns"] = [
                plan["measure"]
            ]

            plan["operations"].append(
                "distribution"
            )

            plan["visualization"] = "histogram"

            return plan

        if categorical_columns:

            plan["group_by"] = (
                categorical_columns[0]
            )

            plan["columns"] = [
                plan["group_by"]
            ]

            plan["operations"].append(
                "categorical_distribution"
            )

            plan["visualization"] = "bar"

            return plan

    # =========================================
    # GENERAL ANALYSIS
    # =========================================

    if numerical_columns:

        plan["measure"] = (
            numerical_columns[0]
        )

        plan["columns"] = [
            plan["measure"]
        ]

        plan["operations"].append(
            "statistical_analysis"
        )

        return plan

    if categorical_columns:

        plan["group_by"] = (
            categorical_columns[0]
        )

        plan["columns"] = [
            plan["group_by"]
        ]

        plan["operations"].append(
            "categorical_distribution"
        )

        return plan

    # =========================================
    # NOTHING FOUND
    # =========================================

    plan["status"] = (
        "No suitable columns were identified "
        "for the requested analysis."
    )

    return plan