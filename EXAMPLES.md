# VirtualEugene Examples and Usage Guide

This document provides comprehensive examples of how to use the VirtualEugene Data Analytics Hub. Each module has specific examples that demonstrate its capabilities.

## Quick Start Examples

### 1. Data Cleaning Module Example

**Scenario**: Clean and prepare employee data for analysis

1. Go to the "Data Cleaning" tab
2. Upload `sample_data.csv` (provided in the repository)
3. Follow the guided cleaning process:
   - Remove duplicates
   - Handle missing values
   - Standardize date formats
   - Validate data types

**Expected Result**: A clean dataset ready for analysis in the EDA and Notebook modules.

### 2. Exploratory Data Analysis (EDA) Example

**Scenario**: Analyze employee performance and salary trends

1. After cleaning data, go to the "EDA" tab
2. Ask questions like:
   - "Show distribution of salary"
   - "Show correlation between age and salary"
   - "Show mean salary by department"
   - "Show scatter plot of experience vs performance"

**Expected Result**: Interactive visualizations and insights about the data patterns.

### 3. Notebook Module Examples

**Scenario**: Advanced data analysis using Python/PySpark

#### Example 1: Basic Data Analysis
```python
# Load the cleaned data (automatically available as 'df')
print("Dataset shape:", df.shape)
print("\nColumn info:")
print(df.info())

# Basic statistics
print("\nSummary statistics:")
print(df.describe())
```

#### Example 2: Data Visualization
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Salary distribution by department
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='Department', y='Salary')
plt.title('Salary Distribution by Department')
plt.xticks(rotation=45)
plt.show()
```

#### Example 3: Performance Analysis
```python
# Performance vs Experience correlation
correlation = df['Performance_Score'].corr(df['Years_Experience'])
print(f"Correlation between Performance and Experience: {correlation:.3f}")

# Top performers by department
top_performers = df.groupby('Department')['Performance_Score'].max()
print("\nTop performance scores by department:")
print(top_performers)
```

#### Example 4: PySpark Example
```python
# Convert to Spark DataFrame
spark_df = spark.createDataFrame(df)

# SQL query example
spark_df.createOrReplaceTempView("employees")
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

### 4. ETL Agent Examples

**Scenario**: Create data transformation pipelines

#### Example: Sales Data ETL
1. Upload `sample_sales_data.csv`
2. Transform:
   - Calculate profit margins
   - Group by category
   - Filter high-revenue products
3. Export transformed data

**Sample ETL Code**:
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, round

# Read sales data
sales_df = spark.read.csv("sample_sales_data.csv", header=True, inferSchema=True)

# Add calculated columns
sales_df = sales_df.withColumn(
    "Profit_Margin", 
    round((col("Revenue") - (col("Price") * col("Units_Sold"))) / col("Revenue") * 100, 2)
)

# Filter high-performing products
high_revenue = sales_df.filter(col("Revenue") > 80000)

# Group by category
category_summary = sales_df.groupBy("Category").agg(
    {"Revenue": "sum", "Units_Sold": "sum"}
)

category_summary.show()
```

### 5. Resource Hub Examples

**Search Examples**:
- "pandas groupby" - Get examples of grouping data
- "matplotlib histogram" - Learn how to create histograms
- "data cleaning techniques" - Best practices for cleaning data
- "PySpark joins" - How to join DataFrames in PySpark

### 6. Prompt Builder Examples

**Example Prompts**:

1. **Data Analysis Prompt**:
   "Analyze the relationship between employee experience and performance scores. Create visualizations and provide insights about career progression patterns."

2. **Business Intelligence Prompt**:
   "Generate a comprehensive sales report showing top-performing products, seasonal trends, and customer segment analysis."

3. **Data Quality Prompt**:
   "Identify data quality issues in the employee dataset and recommend cleaning strategies for missing values, outliers, and inconsistent formats."

## Advanced Examples

### Multi-Module Workflow

**Complete Data Science Pipeline**:

1. **Data Cleaning**: Upload and clean employee data
2. **EDA**: Explore patterns and relationships
3. **Notebook**: Build predictive models
4. **ETL**: Create automated data pipelines
5. **Export**: Download results and reports

### Custom Analysis Examples

#### Salary Prediction Model
```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Prepare features
X = df[['Age', 'Years_Experience', 'Performance_Score']]
y = df['Salary']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Metrics
print(f"R² Score: {r2_score(y_test, y_pred):.3f}")
print(f"RMSE: {mean_squared_error(y_test, y_pred)**0.5:.2f}")
```

#### Department Performance Dashboard
```python
import plotly.express as px
import plotly.graph_objects as go

# Create interactive dashboard
fig1 = px.box(df, x='Department', y='Salary', title='Salary Distribution by Department')
fig2 = px.scatter(df, x='Years_Experience', y='Performance_Score', 
                  color='Department', title='Experience vs Performance')
fig3 = px.histogram(df, x='Age', color='Department', title='Age Distribution')

# Display all charts
fig1.show()
fig2.show()
fig3.show()
```

## Tips and Best Practices

1. **Start with Data Cleaning**: Always clean your data first for better analysis results
2. **Use EDA for Quick Insights**: Get familiar with your data before diving into complex analysis
3. **Leverage the Knowledge Base**: Search for examples when you're stuck
4. **Export Your Work**: Save your cleaned data and analysis results
5. **Combine Modules**: Use multiple modules together for comprehensive analysis

## Troubleshooting Common Issues

### Data Loading Issues
- Ensure CSV files have proper headers
- Check for special characters in data
- Verify file encoding (UTF-8 recommended)

### Visualization Problems
- Make sure data types are correct
- Handle missing values before plotting
- Check column names for typos

### Performance Issues
- Limit data display to first 1000 rows for large datasets
- Use sampling for initial exploration
- Consider using PySpark for big data processing

## Sample Datasets Included

1. **sample_data.csv**: Employee data with demographics, performance, and salary information
2. **sample_sales_data.csv**: Product sales data with revenue, discounts, and customer segments

These datasets are perfect for testing all modules and learning the platform capabilities.