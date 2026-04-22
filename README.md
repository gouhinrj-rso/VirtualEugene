# VirtualEugene

## Solution Overview

### Tech Stack: Streamlit (frontend and backend), pandas (data processing), Matplotlib/Seaborn (visualizations), PySpark (Databricks-like functionality), openpyxl/xlsxwriter (Excel exports), SQLite (lightweight database for data dictionary and knowledge base). All free or built-in, except Streamlit hosting (free on Community Cloud).
### Deployment: Push to a public GitHub repo, then deploy to Streamlit Community Cloud with one-click setup.

## 🚀 Live Examples and Demos

**Try the platform immediately with these examples:**

### 📊 Quick Start Examples

1. **Employee Data Analysis**
   - Load sample employee dataset (15 records)
   - Analyze salary distributions by department
   - Explore performance vs experience correlations
   - Create interactive visualizations

2. **Sales Data Analysis** 
   - Load sample sales dataset (15 products)
   - Analyze revenue patterns by category
   - Find top-performing products
   - Examine discount impact on sales

3. **Natural Language EDA**
   - Ask: "Show distribution of salary"
   - Ask: "Compare revenue by category"
   - Ask: "Find outliers in performance scores"
   - Ask: "Show correlation matrix"

### 💻 Code Examples

#### Notebook Module Examples
```python
# Quick data overview
print("Dataset shape:", df.shape)
print("\nColumn info:")
print(df.info())
print("\nSummary statistics:")
print(df.describe())

# Advanced visualization
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Department salary analysis
dept_stats = df.groupby('Department')['Salary'].agg(['mean', 'count', 'std'])
print(dept_stats)
```

#### PySpark Examples
```python
# Convert to Spark DataFrame
spark_df = spark.createDataFrame(df)
spark_df.createOrReplaceTempView("employees")

# SQL analysis
result = spark.sql("""
    SELECT Department, 
           AVG(Salary) as avg_salary,
           COUNT(*) as employee_count
    FROM employees 
    GROUP BY Department
    ORDER BY avg_salary DESC
""")
result.show()
```

### 🎯 Module-by-Module Examples

#### 1. Data Cleaning Module
- **Sample CSV files included**: `sample_data.csv`, `sample_sales_data.csv`
- **Guided cleaning process**: Remove duplicates, handle missing values, validate data types
- **Export options**: Download cleaned data as CSV or Excel

#### 2. EDA (Exploratory Data Analysis)
- **Natural language queries**: "Show distribution of X", "Compare Y by Z"
- **Auto-generated visualizations**: Histograms, box plots, scatter plots, correlation matrices
- **Statistical insights**: Outlier detection, correlation analysis, summary statistics

#### 3. Notebook Module
- **Pre-loaded libraries**: pandas, numpy, matplotlib, seaborn, PySpark
- **Code suggestions**: Context-aware snippets based on your data
- **Multiple outputs**: Console output, DataFrames, visualizations
- **Export capabilities**: Download results as CSV/Excel

#### 4. ETL Assistant
- **Sample pipelines**: Data transformation workflows
- **Spark integration**: Big data processing capabilities
- **Export options**: Multiple output formats

#### 5. Resource Hub
- **Searchable knowledge base**: Guides for pandas, matplotlib, PySpark
- **Code examples**: Ready-to-use snippets
- **Best practices**: Data science methodologies

## Features

### Resource Hub: Searchable knowledge base with guides for pandas, Python, Matplotlib, Data Analytics, PySpark, Databricks, and Excel.
#### Prompt Builder: Interactive chatbot-style interface to create custom prompts with examples.
#### Notebook Module: Jupyter-like environment for running Python/PySpark code, mimicking Databricks.
#### Coding Assistant: Uses OpenAI's API to answer data science questions and suggest code snippets.
#### Data Dictionary Upload: Upload CSV with Databricks cluster metadata (databases, tables, fields, relationships) for field/table searches and recommendations.
#### Data Cleaning Module: Upload CSV, guided cleaning with pandas/PySpark, output a clean table.
#### EDA Module: Use cleaned table to ask questions, auto-generate Python code for visualizations, and get analysis suggestions.

#### ETL Agent: Query the data dictionary and receive step-by-step joins and transformations for optimized datasets.
### Export: Any rendered DataFrame/table can be exported as CSV or Excel.

## Getting Started

### Option 1: Try Sample Data (Recommended)
1. Run the application: `streamlit run app.py`
2. In the **Overview** tab, click "Load Sample Employee Data" or "Load Sample Sales Data"
3. Explore the data using different tabs (EDA, Notebook, etc.)
4. Follow the guided examples in each module

### Option 2: Upload Your Own Data
1. Go to the **Data Cleaning** tab
2. Upload your CSV file
3. Follow the cleaning workflow
4. Use cleaned data in other modules

### Example Workflows

#### Complete Data Science Pipeline
1. **Data Cleaning**: Upload `sample_data.csv` → Clean and validate
2. **EDA**: Ask "Show salary distribution by department" 
3. **Notebook**: Build performance prediction models
4. **Export**: Download analysis results

#### Business Intelligence Analysis
1. **Load Sales Data**: Use `sample_sales_data.csv`
2. **EDA Analysis**: "Compare revenue by category", "Find top products"
3. **ETL Processing**: Create aggregated reports
4. **Dashboard**: Combine visualizations for insights




## Code Structure
The app will be split into modular Python files for clarity, with a main app.py to tie everything together. Here's the structure:

##### app.py: Main Streamlit app, orchestrates UI and navigation.
##### knowledge_base.py: Manages the searchable resource hub.
##### prompt_builder.py: Handles interactive prompt creation.
##### notebook.py: Implements the Databricks/Jupyter-like code execution.
##### openai_agent.py: Wraps calls to the OpenAI API for agent responses.
##### data_dictionary.py: Processes CSV data dictionary uploads and searches.
##### data_cleaning.py: Guides CSV cleaning and transformation.
##### eda.py: Handles exploratory data analysis and visualization.
##### agents.py: Provides an OpenAI-powered assistant.
##### requirements.txt: Lists dependencies for deployment.
##### SQLite database (app.db) for storing knowledge base and data dictionary.

## Implementation
Below is the complete code for the app. Each module is designed to be modular and reusable, with Streamlit providing the interactive UI. I'll include comments for clarity and instructions for deployment at the end.


## OpenAI API Key Setup
Some features use OpenAI's API. Install requirements and provide an API key through an environment variable.

### Using shell environment
```bash
export OPENAI_API_KEY=sk-...
```

### Using a `.env` file
Create a `.env` file (use `.env.example` as a template) with the following line:

```
OPENAI_API_KEY=sk-...
```

The application will raise an error at startup if this key is not supplied.

