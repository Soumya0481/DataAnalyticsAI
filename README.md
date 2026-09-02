# 📊 Universal Data Analytics Dashboard

A powerful and interactive **Data Analytics Dashboard built with Python and Streamlit** that allows users to upload CSV or Excel datasets, explore their data, perform statistical analysis, generate visualizations, detect anomalies, and ask analytical questions using natural language.

The project is designed to make data analysis easier for users without requiring them to write SQL or Python code.

---

## 🚀 Live Demo

🌐 https://unidataanalyticsai.streamlit.app/

---

## 🎯 Project Objective

The main objective of this project is to provide a **universal data analytics platform** where users can upload structured datasets and analyze them through an interactive dashboard.

Instead of manually writing code for every dataset, users can:

- Upload CSV or Excel files
- Automatically explore dataset structure
- Check data quality
- Analyze statistics
- Create visualizations
- Study correlations
- Detect anomalies
- Ask analytical questions in natural language

---

## ✨ Key Features

### 📂 1. Dataset Upload

Upload structured datasets in:

- CSV format
- Excel (.xlsx) format

The dashboard automatically loads the uploaded dataset for analysis.

---

### 📊 2. Dataset Overview

Quickly understand the uploaded dataset with:

- Number of rows
- Number of columns
- Numerical columns
- Categorical columns
- Dataset preview
- Column information

---

### 🧹 3. Data Quality Analysis

Analyze the quality of your dataset using:

- Missing value detection
- Duplicate record detection
- Empty column detection
- Unique value analysis
- Overall data health

---

### 📈 4. Statistical Analysis

Perform statistical analysis on numerical data including:

- Mean
- Median
- Minimum
- Maximum
- Sum
- Count
- Statistical summaries
- Categorical distributions

---

### 📉 5. Interactive Visualizations

Generate interactive charts using Plotly.

Supported visualizations include:

- Bar charts
- Line charts
- Pie charts
- Scatter plots
- Histograms

Charts are generated based on the selected data and analytical requirement.

---

### 🔗 6. Correlation Analysis

Analyze relationships between numerical variables using correlation analysis and interactive scatter visualizations.

Example:

```text
Show relationship between study hours and exam score.
🚨 7. Anomaly Detection

Identify unusual or potentially abnormal numerical values in the dataset.

This can help users discover:

Unusual records
Extreme values
Potential outliers
Unexpected patterns
💬 Ask Your Data

One of the main features of this project is the Ask Your Data interface.

Users can ask analytical questions in natural language instead of writing Python or SQL queries.

The system analyzes the question and attempts to determine:

What the user wants to calculate
Which dataset columns are relevant
Which analytical operation is required
Whether grouping is required
Whether visualization is requested
🧠 Example Questions

The examples below demonstrate the types of analytical questions users can ask.

🎓 Education / Student Dataset

If you upload a student dataset, you can ask questions such as:

How many students are there?
What is the average score?
What is the maximum score?
What is the minimum score?
Show average score by class.
Show students by gender.
Show a bar chart of students by class.
Show a pie chart of students by gender.
Show a scatter plot of study hours and score.
🏨 Hotel Dataset

Example questions:

How many bookings are there?
What is the average ADR?
What is the maximum lead time?
What is the median lead time?
Show average ADR by hotel.
Show cancellation rate by hotel.
Show a bar chart of bookings by hotel.
Show a pie chart of bookings by hotel.
💼 Business / Sales Dataset

Example questions:

What is the total sales?
What is the average sales?
Which product has the highest sales?
What is the minimum sales value?
Show sales by category.
Show a bar chart of sales by product.
Show a line chart of sales over time.
📋 Work Items / Operational Dataset

Example questions:

How many work items are there?
How many items are open?
Show work items by status.
Show work items by type.
Which status has the highest number of items?
Show a bar chart of work items by status.
📌 General Questions

For any suitable structured dataset, users can ask questions such as:

How many records are there?
What is the average of [column]?
What is the maximum [column]?
What is the minimum [column]?
What is the median of [column]?
What is the total of [column]?
Show [metric] by [category].
Show a bar chart of [metric] by [category].
Show a line chart of [metric] over time.
Show a scatter plot of [column 1] and [column 2].
🛠️ Technology Stack
Python
Streamlit
Pandas
NumPy
Plotly
OpenPyXL
📁 Project Structure
DataAnalyticsAI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── modules/
    ├── data_loader.py
    ├── analytics.py
    ├── data_quality.py
    ├── insights.py
    ├── anomaly.py
    ├── ai_analyst.py
    │
    └── query_engine/
        ├── query_engine.py
        ├── query_parser.py
        ├── metric_resolver.py
        ├── analysis_planner.py
        └── analysis_executor.py
⚙️ Installation

Clone the repository:

git clone https://github.com/Soumya0481/DataAnalyticsAI.git

Move into the project directory:

cd DataAnalyticsAI

Create a virtual environment:

python -m venv .venv

Activate the virtual environment on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py
📦 Requirements

The project uses the following Python packages:

streamlit
pandas
numpy
plotly
openpyxl
🔄 Application Workflow
Upload Dataset
       ↓
Dataset Validation
       ↓
Data Exploration
       ↓
Data Quality Analysis
       ↓
Statistical Analysis
       ↓
Visualization / Correlation / Anomaly Detection
       ↓
Ask Your Data
       ↓
Natural Language Query Analysis
       ↓
Metric & Column Detection
       ↓
Analysis Planning
       ↓
Result / Visualization
🎯 Why This Project?

Traditional data analysis often requires users to:

Write Python code
Write SQL queries
Understand data structures
Manually create charts
Perform repetitive calculations

This project provides an interactive alternative where users can upload their dataset and perform common analytical tasks through a single dashboard.

👨‍💻 Skills Demonstrated

This project demonstrates practical skills in:

Data Analysis
Data Cleaning
Exploratory Data Analysis (EDA)
Statistical Analysis
Data Visualization
Correlation Analysis
Anomaly Detection
Natural Language Query Processing
Python Programming
Pandas
Streamlit
Plotly
Modular Application Development
📌 Supported Dataset Types

The dashboard is designed for structured/tabular datasets such as:

Student / Education data
Sales data
Business data
Hotel data
Customer data
Employee data
Operational data
Financial data
Survey data
Transaction data

The quality of the analysis depends on the structure and column information available in the uploaded dataset.

🌟 Future Improvements

Possible future enhancements include:

More advanced natural-language query understanding
Automatic date/time analysis
Advanced statistical testing
More visualization types
Automated dashboard generation
Advanced forecasting
Custom filtering and drill-down analysis
Multi-dataset analysis

AUTHOR
SOUMYA

📄 License

This project is created for educational, portfolio, and data analytics learning purposes.

⭐ Project

Universal Data Analytics Dashboard

Built with Python, Pandas, Plotly and Streamlit.


**Bas:** `README.md` ka pura old content delete karke ye paste karo → save → `git add README.md` → commit → push.

Is README mein **kisi ek dataset ko project ka limitation nahi banaya hai**, aur examples bhi Education + Hotel + Business + Work Items cover kar rahe hain.
