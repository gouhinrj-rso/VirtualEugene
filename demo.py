#!/usr/bin/env python3
"""
VirtualEugene Demo Script
========================

This script demonstrates the key features and capabilities of VirtualEugene
Data Analytics Hub. It shows how to use the sample data and examples.

Run this script to see what VirtualEugene can do!
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def demo_data_loading():
    """Demonstrate data loading capabilities"""
    print("="*60)
    print("🔄 DEMO: Data Loading")
    print("="*60)
    
    # Load sample employee data
    try:
        df_employees = pd.read_csv('sample_data.csv')
        print(f"✅ Loaded employee data: {len(df_employees)} records")
        print("\nEmployee Data Preview:")
        print(df_employees.head())
        print(f"\nColumns: {list(df_employees.columns)}")
    except FileNotFoundError:
        print("❌ Employee sample data not found")
    
    # Load sample sales data
    try:
        df_sales = pd.read_csv('sample_sales_data.csv')
        print(f"\n✅ Loaded sales data: {len(df_sales)} records")
        print("\nSales Data Preview:")
        print(df_sales.head())
        print(f"\nColumns: {list(df_sales.columns)}")
    except FileNotFoundError:
        print("❌ Sales sample data not found")
    
    return df_employees, df_sales

def demo_eda_analysis(df):
    """Demonstrate EDA capabilities"""
    print("\n" + "="*60)
    print("📊 DEMO: Exploratory Data Analysis")
    print("="*60)
    
    # Basic statistics
    print("📈 Basic Statistics:")
    print(df.describe())
    
    # Data types and info
    print("\n📋 Data Information:")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Data types:\n{df.dtypes}")
    print(f"Missing values:\n{df.isnull().sum()}")
    
    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    print(f"\n🔢 Numeric columns: {numeric_cols}")
    print(f"📝 Categorical columns: {cat_cols}")
    
    return numeric_cols, cat_cols

def demo_visualizations(df, title="Sample Data"):
    """Demonstrate visualization capabilities"""
    print(f"\n📊 Creating visualizations for {title}...")
    
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if len(numeric_cols) >= 1:
        # Distribution plot
        plt.figure(figsize=(12, 8))
        
        if len(numeric_cols) >= 2:
            plt.subplot(2, 2, 1)
            plt.hist(df[numeric_cols[0]], bins=20, alpha=0.7)
            plt.title(f'Distribution of {numeric_cols[0]}')
            plt.xlabel(numeric_cols[0])
            plt.ylabel('Frequency')
            
            plt.subplot(2, 2, 2)
            if len(cat_cols) >= 1:
                df.boxplot(column=numeric_cols[0], by=cat_cols[0], ax=plt.gca())
                plt.title(f'{numeric_cols[0]} by {cat_cols[0]}')
            
            plt.subplot(2, 2, 3)
            correlation_matrix = df[numeric_cols].corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
            plt.title('Correlation Matrix')
            
            plt.subplot(2, 2, 4)
            if len(cat_cols) >= 1:
                df[cat_cols[0]].value_counts().plot(kind='bar')
                plt.title(f'Distribution of {cat_cols[0]}')
                plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(f'demo_{title.lower().replace(" ", "_")}_analysis.png', dpi=150, bbox_inches='tight')
        print(f"✅ Saved visualization: demo_{title.lower().replace(' ', '_')}_analysis.png")
        plt.close()

def demo_notebook_examples():
    """Demonstrate Notebook module capabilities"""
    print("\n" + "="*60)
    print("💻 DEMO: Notebook Module Examples")
    print("="*60)
    
    print("🐍 Python Code Examples:")
    print("""
# Example 1: Load and explore data
df = pd.read_csv('sample_data.csv')
print(f"Dataset shape: {df.shape}")
print(df.info())
print(df.describe())

# Example 2: Advanced visualization
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Department', y='Salary')
plt.title('Salary Distribution by Department')
plt.xticks(rotation=45)
plt.show()

# Example 3: Statistical analysis
correlation = df['Performance_Score'].corr(df['Years_Experience'])
print(f"Performance vs Experience correlation: {correlation:.3f}")

# Example 4: Group analysis
dept_stats = df.groupby('Department')['Salary'].agg(['mean', 'count', 'std'])
print(dept_stats)
""")

def demo_etl_examples():
    """Demonstrate ETL capabilities"""
    print("\n" + "="*60)
    print("🔄 DEMO: ETL (Extract, Transform, Load) Examples")
    print("="*60)
    
    print("⚡ PySpark Code Examples:")
    print("""
# Example 1: Load data with Spark
spark_df = spark.read.csv('sample_data.csv', header=True, inferSchema=True)
spark_df.show(5)

# Example 2: Data transformations
from pyspark.sql import functions as F

# Add calculated columns
spark_df = spark_df.withColumn('Experience_Level', 
    F.when(F.col('Years_Experience') < 3, 'Junior')
     .when(F.col('Years_Experience') < 8, 'Mid-level')
     .otherwise('Senior'))

# Example 3: SQL operations
spark_df.createOrReplaceTempView('employees')
result = spark.sql('''
    SELECT Department, 
           AVG(Salary) as avg_salary,
           COUNT(*) as employee_count
    FROM employees 
    GROUP BY Department
    ORDER BY avg_salary DESC
''')
result.show()

# Example 4: Export results
result.toPandas().to_csv('department_summary.csv', index=False)
""")

def demo_natural_language_queries():
    """Demonstrate natural language EDA queries"""
    print("\n" + "="*60)
    print("🗣️ DEMO: Natural Language EDA Queries")
    print("="*60)
    
    print("💬 Example queries you can ask in the EDA module:")
    
    queries = [
        "Show distribution of salary",
        "Compare performance by department", 
        "Find outliers in years of experience",
        "Show correlation matrix",
        "Create scatter plot of experience vs performance",
        "Show mean salary by department",
        "Find data summary",
        "Compare revenue by category",  # For sales data
        "Show distribution of discount percent",  # For sales data
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"{i:2d}. \"{query}\"")
    
    print("\n🎯 These queries will automatically:")
    print("   • Generate appropriate visualizations")
    print("   • Provide statistical summaries")  
    print("   • Suggest next analysis steps")
    print("   • Show relevant code snippets")

def main():
    """Main demo function"""
    print("🚀 VirtualEugene Data Analytics Hub - DEMO")
    print("=" * 60)
    print("This demo shows the capabilities of VirtualEugene")
    print("Web app: http://localhost:8501")
    print()
    
    # Demo 1: Data loading
    try:
        df_employees, df_sales = demo_data_loading()
        
        # Demo 2: EDA analysis
        if 'df_employees' in locals():
            print("\n👥 Employee Data Analysis:")
            emp_numeric, emp_cat = demo_eda_analysis(df_employees)
            demo_visualizations(df_employees, "Employee Data")
        
        if 'df_sales' in locals():
            print("\n💰 Sales Data Analysis:")
            sales_numeric, sales_cat = demo_eda_analysis(df_sales)
            demo_visualizations(df_sales, "Sales Data")
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
    
    # Demo 3: Code examples
    demo_notebook_examples()
    demo_etl_examples()
    demo_natural_language_queries()
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE!")
    print("="*60)
    print("🌐 Open http://localhost:8501 to try the interactive web interface")
    print("📚 Check EXAMPLES.md for detailed tutorials")
    print("📖 See README.md for complete documentation")

if __name__ == "__main__":
    main()