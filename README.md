# 📊 Universal Data Analytics Dashboard

A powerful Streamlit-based data analytics platform that allows users to upload CSV or Excel datasets and explore them through interactive analytics and natural-language queries.

## 🚀 Features

- 📂 Upload CSV and Excel datasets
- 📊 Dataset overview and statistics
- 🧹 Data quality analysis
- 🔍 Missing value and duplicate detection
- 📈 Interactive visualizations
- 🔗 Correlation analysis
- 🚨 Anomaly detection
- 💬 Natural-language data queries
- 📊 Automatic chart selection
- 📋 Statistical analysis
- 🏷️ Categorical and numerical analysis
- 🔄 Dataset-independent analytical workflow

## 💬 Ask Your Data

Users can ask questions in natural language, such as:

- What is the average ADR?
- What is the maximum lead time?
- What is the cancellation rate?
- Show me a bar chart of cancellation rate by hotel.
- Show me a pie chart of bookings by hotel.
- Show me a line chart of bookings by hotel.
- Show me a scatter plot of lead time and ADR.

The system analyzes the question, identifies relevant columns, creates an analytical plan, executes the analysis, and presents the result.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- OpenPyXL

## 📁 Project Structure

```text
DataAnalyticsAI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── modules/
    ├── analytics.py
    ├── anomaly.py
    ├── data_loader.py
    ├── data_quality.py
    ├── data_questions.py
    ├── insights.py
    ├── ai_analyst.py
    │
    └── query_engine/
        ├── query_engine.py
        ├── query_parser.py
        ├── column_matcher.py
        ├── metric_resolver.py
        ├── analysis_planner.py
        ├── analysis_executor.py
        ├── chart_selector.py
        └── schema_analyzer.py

▶️ Run Locally

Install the required dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py
🎯 Project Goal

The goal of this project is to create a universal data analytics platform that can work with different types of structured datasets without depending on a single predefined dataset.

Users can upload their own data and interact with it through analytics, visualizations, and natural-language questions.

👨‍💻 Author

Soumya


### Then run these commands:

```powershell
git add README.md
git commit -m "Add project documentation"
git push
