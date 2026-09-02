from .schema_analyzer import analyze_schema
from .query_parser import parse_query
from .column_matcher import match_columns
from .metric_resolver import resolve_metric
from .analysis_planner import create_analysis_plan
from .analysis_executor import execute_analysis
from .chart_selector import select_chart


def process_user_query(df, question):
    """
    Complete natural-language data analysis pipeline.

    Dataset
        ↓
    Schema
        ↓
    Question
        ↓
    Column Matching
        ↓
    Metric Resolution
        ↓
    Analysis Planning
        ↓
    Execution
        ↓
    Chart Selection
    """

    # =========================================
    # 1. UNDERSTAND DATASET
    # =========================================

    schema = analyze_schema(df)

    # =========================================
    # 2. UNDERSTAND USER QUESTION
    # =========================================

    parsed_query = parse_query(
        question
    )

    # =========================================
    # 3. FIND RELEVANT COLUMNS
    # =========================================

    matched_columns = match_columns(
        df,
        schema,
        question,
        parsed_query
    )

    # =========================================
    # 4. RESOLVE METRIC
    # =========================================

    metric = resolve_metric(
        question,
        matched_columns,
        schema,
        parsed_query,
        df
    )
    print("DEBUG METRIC:", metric)
    # =========================================
    # 5. CREATE ANALYSIS PLAN
    # =========================================

    plan = create_analysis_plan(
        schema,
        parsed_query,
        matched_columns,
        metric
    )

    # =========================================
    # 6. ADD METRIC INFORMATION TO PLAN
    # =========================================

    plan["metric"] = metric

    if metric.get("column"):

        plan["measure"] = (
            metric["column"]
        )

        if metric["column"] not in plan["columns"]:

            plan["columns"].append(
                metric["column"]
            )

    # =========================================
    # 7. EXECUTE ANALYSIS
    # =========================================

    execution_result = execute_analysis(
        df,
        plan
    )

    result_data = execution_result.get(
        "data"
    )

    # =========================================
    # 8. SELECT CHART
    # =========================================

    chart_type = select_chart(
        result_data,
        parsed_query,
        plan
    )

    # =========================================
    # 9. RETURN COMPLETE RESULT
    # =========================================

    return {
        "schema": schema,
        "parsed_query": parsed_query,
        "matched_columns": matched_columns,
        "metric": metric,
        "plan": plan,
        "result": result_data,
        "chart_type": chart_type,
        "message": execution_result.get(
            "message",
            ""
        )
    }