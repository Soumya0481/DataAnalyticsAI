import streamlit as st
import plotly.express as px
import pandas as pd
import colorsys

from modules.data_loader import (
    load_data,
    get_data_quality
)

from modules.analytics import (
    get_column_information,
    get_numeric_columns,
    get_categorical_columns,
    get_statistical_summary,
    get_categorical_distribution,
    get_correlation_matrix
)

from modules.data_quality import (
    get_missing_values,
    get_duplicate_count,
    get_empty_columns,
    get_unique_values,
    get_data_health
)

from modules.insights import generate_insights
from modules.anomaly import detect_anomalies
from modules.ai_analyst import generate_ai_analysis

# =========================================
# UNIVERSAL QUERY ENGINE
# =========================================

from modules.query_engine.query_engine import (
    process_user_query
)


# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="AI Data Analytics",
    page_icon="📊",
    layout="wide"
)


# =========================================
# CUSTOM CSS
# =========================================

st.markdown(
    """
    <style>

    [data-testid="stSidebar"] {
        min-width: 280px;
        max-width: 280px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================
# HEADER
# =========================================

st.title("📊 AI-Powered Data Analytics")

st.caption(
    "Upload your dataset and explore it your way."
)


# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.header("📊 Analytics Menu")

    uploaded_file = st.file_uploader(
        "📂 Upload Dataset",
        type=[
            "csv",
            "xlsx",
            "xls"
        ]
    )

    if uploaded_file is not None:

        page = st.radio(
            "Explore",
            [
                "🏠 Overview",
                "🧹 Data Quality",
                "📊 Statistics",
                "📈 Visualization",
                "🔗 Correlation",
                "🧠 AI Insights",
                "🚨 Anomalies",
                "🤖 AI Analyst",
                "💬 Ask Your Data"
            ]
        )

    else:

        page = "🏠 Overview"


# =========================================
# NO DATASET
# =========================================

if uploaded_file is None:

    st.info(
        "👈 Upload a CSV or Excel file from "
        "the sidebar to start analyzing your data."
    )

    st.stop()


# =========================================
# LOAD DATA
# =========================================

try:

    df = load_data(
        uploaded_file
    )

    st.success(
        "✅ Dataset uploaded successfully!"
    )


    # =========================================
    # OVERVIEW
    # =========================================

    if page == "🏠 Overview":

        st.header(
            "🏠 Dataset Overview"
        )

        st.write(
            "Here's a quick summary of "
            "your uploaded dataset."
        )

        quality = get_data_quality(
            df
        )

        col1, col2, col3, col4 = st.columns(
            4
        )

        with col1:

            st.metric(
                "Rows",
                quality["rows"]
            )

        with col2:

            st.metric(
                "Columns",
                quality["columns"]
            )

        with col3:

            st.metric(
                "Missing Values",
                quality["missing_values"]
            )

        with col4:

            st.metric(
                "Duplicate Rows",
                quality["duplicate_rows"]
            )


        st.subheader(
            "📋 Dataset Preview"
        )

        st.dataframe(
            df.head(10),
            use_container_width=True
        )


        st.subheader(
            "🔍 Column Information"
        )

        column_info = get_column_information(
            df
        )

        st.dataframe(
            column_info,
            use_container_width=True
        )


    # =========================================
    # DATA QUALITY
    # =========================================

    elif page == "🧹 Data Quality":

        st.header(
            "🧹 Data Quality"
        )

        st.write(
            "Check the quality and reliability "
            "of your dataset."
        )

        health_score = get_data_health(
            df
        )

        st.subheader(
            "❤️ Overall Data Health"
        )

        if health_score >= 90:

            st.success(
                f"Excellent — {health_score}% data health"
            )

        elif health_score >= 70:

            st.warning(
                f"Good — {health_score}% data health"
            )

        else:

            st.error(
                f"Needs attention — "
                f"{health_score}% data health"
            )


        missing_total = int(
            df.isnull().sum().sum()
        )

        duplicate_total = (
            get_duplicate_count(df)
        )

        empty_columns = (
            get_empty_columns(df)
        )


        col1, col2, col3 = st.columns(
            3
        )

        with col1:

            st.metric(
                "Missing Values",
                missing_total
            )

        with col2:

            st.metric(
                "Duplicate Rows",
                duplicate_total
            )

        with col3:

            st.metric(
                "Empty Columns",
                len(empty_columns)
            )


        st.subheader(
            "🔎 Missing Values by Column"
        )

        missing_data = (
            get_missing_values(df)
        )

        st.dataframe(
            missing_data,
            use_container_width=True
        )


        st.subheader(
            "🔢 Unique Values"
        )

        unique_data = (
            get_unique_values(df)
        )

        st.dataframe(
            unique_data,
            use_container_width=True
        )


        st.subheader(
            "🗑️ Empty Columns"
        )

        if empty_columns:

            for column in empty_columns:

                st.warning(
                    f"Column '{column}' "
                    "contains no data."
                )

        else:

            st.success(
                "✅ No completely empty "
                "columns found."
            )


    # =========================================
    # STATISTICS
    # =========================================

    elif page == "📊 Statistics":

        st.header(
            "📊 Statistical Analysis"
        )

        st.write(
            "Explore the statistical characteristics "
            "of your numerical data."
        )

        numeric_columns = (
            get_numeric_columns(df)
        )

        if numeric_columns:

            statistics = (
                get_statistical_summary(df)
            )

            st.subheader(
                "📈 Statistical Summary"
            )

            st.dataframe(
                statistics.round(2),
                use_container_width=True
            )


            st.subheader(
                "🔎 Explore a Column"
            )

            selected_column = st.selectbox(
                "Choose a numerical column",
                numeric_columns,
                key="statistics_column"
            )

            selected_data = (
                df[selected_column]
            )


            st.subheader(
                "📊 Key Metrics"
            )

            col1, col2, col3, col4 = (
                st.columns(4)
            )

            with col1:

                st.metric(
                    "Mean",
                    round(
                        selected_data.mean(),
                        2
                    )
                )

            with col2:

                st.metric(
                    "Median",
                    round(
                        selected_data.median(),
                        2
                    )
                )

            with col3:

                st.metric(
                    "Minimum",
                    round(
                        selected_data.min(),
                        2
                    )
                )

            with col4:

                st.metric(
                    "Maximum",
                    round(
                        selected_data.max(),
                        2
                    )
                )


            col1, col2, col3 = (
                st.columns(3)
            )

            with col1:

                st.metric(
                    "Standard Deviation",
                    round(
                        selected_data.std(),
                        2
                    )
                )

            with col2:

                st.metric(
                    "25th Percentile",
                    round(
                        selected_data.quantile(0.25),
                        2
                    )
                )

            with col3:

                st.metric(
                    "75th Percentile",
                    round(
                        selected_data.quantile(0.75),
                        2
                    )
                )

        else:

            st.info(
                "No numerical columns available "
                "for statistical analysis."
            )


    # =========================================
    # VISUALIZATION
    # =========================================

    elif page == "📈 Visualization":

        st.header(
            "📈 Data Visualization"
        )

        st.write(
            "Choose what you want to visualize."
        )

        numeric_columns = (
            get_numeric_columns(df)
        )

        categorical_columns = (
            get_categorical_columns(df)
        )


        visualization_type = st.selectbox(
            "Choose visualization category",
            [
                "Numerical Data",
                "Categorical Data"
            ]
        )


        # =====================================
        # NUMERICAL
        # =====================================

        if visualization_type == "Numerical Data":

            if numeric_columns:

                chart_type = st.selectbox(
                    "Choose chart type",
                    [
                        "Histogram",
                        "Box Plot",
                        "Line Chart"
                    ]
                )


                selected_column = (
                    st.selectbox(
                        "Choose numerical column",
                        numeric_columns
                    )
                )


                chart_color = st.color_picker(
                    "🎨 Choose chart color",
                    "#1f77b4"
                )


                if chart_type == "Histogram":

                    fig = px.histogram(
                        df,
                        x=selected_column,
                        title=(
                            f"Distribution of "
                            f"{selected_column}"
                        )
                    )

                    fig.update_traces(
                        marker_color=chart_color
                    )


                elif chart_type == "Box Plot":

                    fig = px.box(
                        df,
                        y=selected_column,
                        title=(
                            f"Box Plot of "
                            f"{selected_column}"
                        )
                    )

                    fig.update_traces(
                        marker_color=chart_color
                    )


                else:

                    fig = px.line(
                        df,
                        y=selected_column,
                        title=(
                            f"{selected_column} Trend"
                        )
                    )

                    fig.update_traces(
                        line_color=chart_color
                    )


                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.warning(
                    "No numerical columns found."
                )


        # =====================================
        # CATEGORICAL
        # =====================================

        else:

            if categorical_columns:

                chart_type = st.selectbox(
                    "Choose chart type",
                    [
                        "Bar Chart",
                        "Pie Chart"
                    ]
                )


                selected_category = (
                    st.selectbox(
                        "Choose categorical column",
                        categorical_columns
                    )
                )


                chart_color = st.color_picker(
                    "🎨 Choose chart color",
                    "#636EFA"
                )


                distribution = (
                    get_categorical_distribution(
                        df,
                        selected_category
                    )
                )


                if chart_type == "Bar Chart":

                    fig = px.bar(
                        distribution,
                        x=selected_category,
                        y="Count",
                        title=(
                            f"{selected_category} "
                            "Distribution"
                        )
                    )

                    fig.update_traces(
                        marker_color=chart_color
                    )


                else:

                    base_color = (
                        chart_color.lstrip("#")
                    )

                    r = (
                        int(
                            base_color[0:2],
                            16
                        ) / 255
                    )

                    g = (
                        int(
                            base_color[2:4],
                            16
                        ) / 255
                    )

                    b = (
                        int(
                            base_color[4:6],
                            16
                        ) / 255
                    )

                    h, s, v = (
                        colorsys.rgb_to_hsv(
                            r,
                            g,
                            b
                        )
                    )

                    number_of_slices = (
                        len(distribution)
                    )

                    pie_colors = []

                    for i in range(
                        number_of_slices
                    ):

                        brightness = (
                            0.45
                            + (
                                0.5
                                * i
                                / max(
                                    number_of_slices - 1,
                                    1
                                )
                            )
                        )

                        red, green, blue = (
                            colorsys.hsv_to_rgb(
                                h,
                                s,
                                min(
                                    brightness,
                                    1
                                )
                            )
                        )

                        pie_colors.append(
                            "#{:02x}{:02x}{:02x}".format(
                                int(red * 255),
                                int(green * 255),
                                int(blue * 255)
                            )
                        )


                    fig = px.pie(
                        distribution,
                        names=selected_category,
                        values="Count",
                        title=(
                            f"{selected_category} "
                            "Distribution"
                        )
                    )

                    fig.update_traces(
                        marker=dict(
                            colors=pie_colors
                        )
                    )


                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            else:

                st.warning(
                    "No categorical columns found."
                )


    # =========================================
    # CORRELATION
    # =========================================

    elif page == "🔗 Correlation":

        st.header(
            "🔗 Relationship Analysis"
        )

        st.write(
            "Explore relationships between "
            "numerical columns in your dataset."
        )

        correlation_matrix = (
            get_correlation_matrix(df)
        )

        if correlation_matrix is not None:

            st.subheader(
                "📊 Relationship Results"
            )

            st.dataframe(
                correlation_matrix.round(2),
                use_container_width=True
            )


            with st.expander(
                "🔬 View detailed correlation heatmap"
            ):

                fig = px.imshow(
                    correlation_matrix,
                    text_auto=True,
                    aspect="auto",
                    title="Correlation Heatmap"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        else:

            st.info(
                "At least two numerical columns "
                "are required for relationship analysis."
            )


    # =========================================
    # AI INSIGHTS
    # =========================================

    elif page == "🧠 AI Insights":

        st.header(
            "🧠 AI Insights"
        )

        st.write(
            "Important findings automatically "
            "identified from your uploaded dataset."
        )

        insights = (
            generate_insights(df)
        )


        st.subheader(
            "📌 Dataset Summary"
        )

        for insight in insights["summary"]:

            st.info(
                f"💡 {insight}"
            )


        st.subheader(
            "🔎 Data Quality"
        )

        for insight in insights["quality"]:

            st.success(
                f"✅ {insight}"
            )


        st.subheader(
            "📊 Important Patterns"
        )

        for insight in insights["patterns"]:

            st.warning(
                f"📈 {insight}"
            )


        st.subheader(
            "🔤 Category Insights"
        )

        for insight in insights["categories"]:

            st.info(
                f"🔹 {insight}"
            )


        st.subheader(
            "🔗 Relationship Insights"
        )

        if insights["relationships"]:

            for insight in (
                insights["relationships"]
            ):

                st.info(
                    f"🔗 {insight}"
                )

        else:

            st.info(
                "No strong numerical relationships "
                "were detected."
            )


    # =========================================
    # ANOMALIES
    # =========================================

    elif page == "🚨 Anomalies":

        st.header(
            "🚨 Anomaly Detection"
        )

        st.write(
            "Find numerical values that are "
            "unusually different from the rest "
            "of your dataset."
        )

        anomalies = (
            detect_anomalies(df)
        )


        st.subheader(
            "📊 Analysis Summary"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Potential Anomalies",
                len(anomalies)
            )

        with col2:

            numerical_count = len(
                df.select_dtypes(
                    include="number"
                ).columns
            )

            st.metric(
                "Numerical Columns Checked",
                numerical_count
            )


        if not anomalies.empty:

            st.warning(
                f"⚠️ {len(anomalies)} potential "
                "anomalies were detected."
            )

            st.subheader(
                "🔎 Detected Anomalies"
            )

            st.dataframe(
                anomalies,
                use_container_width=True
            )

            st.info(
                "💡 These values are unusual compared "
                "with the rest of the data. An unusual "
                "value is not automatically an error. "
                "Review it before changing or removing it."
            )

        else:

            st.success(
                "✅ No potential anomalies were detected."
            )

            st.info(
                "🟢 Your numerical data does not contain "
                "values that appear unusually far from "
                "the normal range."
            )

            st.caption(
                "The system checks numerical columns "
                "using the IQR statistical method."
            )


    # =========================================
    # AI ANALYST
    # =========================================

    elif page == "🤖 AI Analyst":

        st.header(
            "🤖 AI Analyst"
        )

        st.write(
            "Get a simple overall analysis of "
            "your uploaded dataset."
        )

        insights = (
            generate_insights(df)
        )

        anomalies = (
            detect_anomalies(df)
        )

        correlation_matrix = (
            get_correlation_matrix(df)
        )

        analysis = generate_ai_analysis(
            df,
            insights,
            anomalies,
            correlation_matrix
        )


        st.subheader(
            "📌 Overall Finding"
        )

        st.info(
            f"💡 {analysis['overview']}"
        )


        st.subheader(
            "🧹 Data Quality"
        )

        st.success(
            f"✅ {analysis['data_quality']}"
        )


        if analysis["patterns"]:

            st.subheader(
                "📊 Important Findings"
            )

            for pattern in (
                analysis["patterns"]
            ):

                st.info(
                    f"📈 {pattern}"
                )


        if analysis["relationships"]:

            st.subheader(
                "🔗 Relationships"
            )

            for relationship in (
                analysis["relationships"]
            ):

                st.info(
                    f"🔗 {relationship}"
                )


        st.subheader(
            "🚨 Anomaly Check"
        )

        if anomalies.empty:

            st.success(
                "✅ No potential numerical "
                "anomalies were detected."
            )

        else:

            st.warning(
                f"⚠️ {len(anomalies)} potential "
                "anomalies were detected."
            )


        st.subheader(
            "⚠️ Data Reliability"
        )

        reliability_messages = (
            analysis.get(
                "reliability",
                []
            )
        )

        if reliability_messages:

            for message in (
                reliability_messages
            ):

                if message.startswith(
                    "⚠️"
                ):

                    st.warning(message)

                elif message.startswith(
                    "❌"
                ):

                    st.error(message)

                else:

                    st.info(message)

        else:

            st.info(
                "No data reliability concerns "
                "were detected."
            )


        st.subheader(
            "💡 Recommendations"
        )

        for recommendation in (
            analysis["recommendations"]
        ):

            st.warning(
                f"💡 {recommendation}"
            )
        # =========================================
    # UNIVERSAL ASK YOUR DATA
    # =========================================

    elif page == "💬 Ask Your Data":

        st.header(
            "💬 Ask Your Data"
        )

        st.write(
            "Ask questions about your uploaded "
            "dataset using natural language."
        )

        st.caption(
            "Ask questions in your own words. "
            "The system analyzes the uploaded "
            "dataset and returns the appropriate "
            "result."
        )

        # =========================================
        # QUESTION INPUT
        # =========================================

        question = st.text_input(
            "🔍 Enter your question",
            placeholder=(
                "Example: What is the cancellation rate?"
            ),
            key="data_question"
        )

        analyze_button = st.button(
            "🔎 Analyze Question",
            type="primary"
        )

        # =========================================
        # ANALYZE
        # =========================================

        if analyze_button:

            if not question.strip():

                st.warning(
                    "Please enter a question first."
                )

            else:

                try:

                    with st.spinner(
                        "🔎 Analyzing your dataset..."
                    ):

                        response = process_user_query(
                            df,
                            question
                        )

                    # =================================
                    # RESPONSE MESSAGE
                    # =================================

                    message = response.get(
                        "message",
                        ""
                    )

                    if message:

                        st.info(message)

                    # =================================
                    # GET RESULT
                    # =================================

                    result = response.get(
                        "result"
                    )

                    metric = response.get(
                        "metric",
                        {}
                    )

                    plan = response.get(
                        "plan",
                        {}
                    )

                    chart_type = response.get(
                        "chart_type"
                    )

                    # =================================
                    # NO RESULT
                    # =================================

                    if result is None:

                        st.warning(
                            "The system could not "
                            "generate a result for "
                            "this question."
                        )

                    elif not hasattr(
                        result,
                        "empty"
                    ):

                        st.warning(
                            "The analysis returned "
                            "an unsupported result."
                        )

                    elif result.empty:

                        st.warning(
                            "The analysis returned "
                            "no data."
                        )

                    else:

                        # =================================
                        # ANALYSIS RESULT
                        # =================================

                        st.subheader(
                            "📊 Analysis Result"
                        )

                        # =================================
                        # OVERALL RATE
                        # =================================

                        if (
                            metric.get("type")
                            == "rate"
                            and plan.get(
                                "group_by"
                            ) is None
                            and "Rate (%)"
                            in result.columns
                        ):

                            rate_value = float(
                                result[
                                    "Rate (%)"
                                ].iloc[0]
                            )

                            st.metric(
                                "📈 Overall Rate",
                                f"{rate_value:.2f}%"
                            )

                            col1, col2 = (
                                st.columns(2)
                            )

                            if (
                                "Total Records"
                                in result.columns
                            ):

                                with col1:

                                    st.metric(
                                        "Total Records",
                                        f"{int(result['Total Records'].iloc[0]):,}"
                                    )

                            if (
                                "Positive Records"
                                in result.columns
                            ):

                                with col2:

                                    st.metric(
                                        "Positive Records",
                                        f"{int(result['Positive Records'].iloc[0]):,}"
                                    )

                        # =================================
                        # SINGLE VALUE ANALYSIS
                        # =================================

                        elif (
                            len(result) == 1
                            and len(result.columns) >= 2
                        ):

                            value_column = (
                                result.columns[-1]
                            )

                            value = result[
                                value_column
                            ].iloc[0]

                            metric_type = (
                                metric.get(
                                    "type",
                                    ""
                                )
                            )

                            metric_labels = {
                                "mean": "📊 Average",
                                "median": "📊 Median",
                                "min": "📉 Minimum",
                                "max": "📈 Maximum",
                                "sum": "➕ Total",
                                "count": "🔢 Count"
                            }

                            label = (
                                metric_labels.get(
                                    metric_type,
                                    "📊 Result"
                                )
                            )

                            if pd.api.types.is_number(
                                value
                            ):

                                if float(value).is_integer():

                                    display_value = (
                                        f"{int(value):,}"
                                    )

                                else:

                                    display_value = (
                                        f"{float(value):,.2f}"
                                    )

                            else:

                                display_value = str(
                                    value
                                )

                            st.metric(
                                label,
                                display_value
                            )

                            st.dataframe(
                                result,
                                use_container_width=True,
                                hide_index=True
                            )

                        # =================================
                        # NORMAL TABLE RESULT
                        # =================================

                        else:

                            st.dataframe(
                                result,
                                use_container_width=True,
                                hide_index=True
                            )

                        # =================================
                        # VISUALIZATION
                        # =================================

                        if (
                            chart_type
                            and result is not None
                            and not result.empty
                        ):

                            columns = (
                                result.columns.tolist()
                            )

                            st.subheader(
                                "📈 Visualization"
                            )

                            # =================================
                            # BAR CHART
                            # =================================

                            if chart_type == "bar":

                                if len(columns) >= 2:

                                    x_column = (
                                        columns[0]
                                    )

                                    if (
                                        "Rate (%)"
                                        in columns
                                    ):

                                        y_column = (
                                            "Rate (%)"
                                        )

                                    else:

                                        numeric_columns = (
                                            result
                                            .select_dtypes(
                                                include="number"
                                            )
                                            .columns
                                            .tolist()
                                        )

                                        if numeric_columns:

                                            y_column = (
                                                numeric_columns[-1]
                                            )

                                        else:

                                            y_column = (
                                                columns[1]
                                            )

                                    fig = px.bar(
                                        result,
                                        x=x_column,
                                        y=y_column,
                                        title=question
                                    )

                                    st.plotly_chart(
                                        fig,
                                        use_container_width=True
                                    )

                            # =================================
                            # LINE CHART
                            # =================================

                            elif chart_type == "line":

                                if len(columns) >= 2:

                                    numeric_columns = (
                                        result
                                        .select_dtypes(
                                            include="number"
                                        )
                                        .columns
                                        .tolist()
                                    )

                                    if numeric_columns:

                                        y_column = (
                                            numeric_columns[-1]
                                        )

                                    else:

                                        y_column = (
                                            columns[1]
                                        )

                                    fig = px.line(
                                        result,
                                        x=columns[0],
                                        y=y_column,
                                        title=question
                                    )

                                    st.plotly_chart(
                                        fig,
                                        use_container_width=True
                                    )

                            # =================================
                            # PIE CHART
                            # =================================

                            elif chart_type == "pie":

                                if len(columns) >= 2:

                                    numeric_columns = (
                                        result
                                        .select_dtypes(
                                            include="number"
                                        )
                                        .columns
                                        .tolist()
                                    )

                                    if numeric_columns:

                                        value_column = (
                                            numeric_columns[-1]
                                        )

                                        fig = px.pie(
                                            result,
                                            names=columns[0],
                                            values=value_column,
                                            title=question
                                        )

                                        st.plotly_chart(
                                            fig,
                                            use_container_width=True
                                        )

                            # =================================
                            # HISTOGRAM
                            # =================================

                            elif chart_type == "histogram":

                                numeric_columns = (
                                    result
                                    .select_dtypes(
                                        include="number"
                                    )
                                    .columns
                                    .tolist()
                                )

                                if numeric_columns:

                                    fig = px.histogram(
                                        result,
                                        x=numeric_columns[0],
                                        title=question
                                    )

                                    st.plotly_chart(
                                        fig,
                                        use_container_width=True
                                    )

                            # =================================
                            # SCATTER
                            # =================================

                            elif chart_type == "scatter":

                                numeric_columns = (
                                    result
                                    .select_dtypes(
                                        include="number"
                                    )
                                    .columns
                                    .tolist()
                                )

                                if len(
                                    numeric_columns
                                ) >= 2:

                                    fig = px.scatter(
                                        result,
                                        x=numeric_columns[0],
                                        y=numeric_columns[1],
                                        title=question
                                    )

                                    st.plotly_chart(
                                        fig,
                                        use_container_width=True
                                    )

                    # =================================
                    # ANALYSIS DETAILS
                    # =================================

                    

                except Exception as e:

                    st.error(
                        f"❌ Analysis failed: {e}"
                    )

    


# =========================================
# GLOBAL ERROR HANDLING
# =========================================

except Exception as e:

    st.error(
        f"❌ Something went wrong: {e}"
    )