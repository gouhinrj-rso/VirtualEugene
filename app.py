# Databricks notebook source
import os
import streamlit as st
import pandas as pd
import openai
from knowledge_base import search_knowledge_base, init_knowledge_base
from prompt_builder import build_prompt
try:
    from notebook import run_notebook
except Exception:  # pragma: no cover
    def run_notebook():
        pass

from data_dictionary import (
    upload_data_dictionary,
    search_data_dictionary,
    init_data_dictionary,
)
from data_cleaning import clean_data

try:
    from eda import perform_eda
except Exception:  # pragma: no cover
    def perform_eda():
        pass

from etl_agent import run_etl_agent

from io import BytesIO

openai.api_key = os.getenv("OPENAI_API_KEY", "")
if not openai.api_key:
    # In test environments the key may be missing; the app can still run
    # for non-LLM features, so we simply warn instead of raising.
    print("Warning: OPENAI_API_KEY environment variable is not set. OpenAI features disabled.")

st.set_page_config(page_title="Data Analytics Hub", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for better style and ergonomics
st.markdown("""
    <style>
    .section-divider { border-top: 1px solid #ddd; margin: 20px 0; }
    .stButton > button { width: 100%; }
    .stExpander { border: 1px solid #ddd; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# Initialize databases
with st.spinner("Initializing resources and prompts from APIs..."):
    init_knowledge_base()
    init_data_dictionary()

# Session state for cleaned data
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None



tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Overview",
    "Data Cleaning",
    "EDA",
    "Notebook",
    "ETL Assistant",
    "Resource Hub",
    "Prompt Builder",
])




with tab1:
    st.header("🏠 VirtualEugene - Data Analytics Hub")
    st.markdown("""
    Welcome to **VirtualEugene**, your comprehensive data analytics platform! 
    This application simulates Databricks/Jupyter functionality with powerful data analysis capabilities.
    """)
    
    # Quick demo section
    st.subheader("🚀 Quick Demo - Try It Now!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Load Sample Employee Data", help="Load employee dataset with 15 records", key="main_load_employee"):
            try:
                sample_df = pd.read_csv('sample_data.csv')
                st.session_state.cleaned_df = sample_df
                st.success(f"✅ Loaded {len(sample_df)} employee records!")
                st.balloons()
            except FileNotFoundError:
                st.error("Sample data file not found.")
    
    with col2:
        if st.button("📊 Load Sample Sales Data", help="Load sales dataset with product information", key="main_load_sales"):
            try:
                sample_df = pd.read_csv('sample_sales_data.csv')
                st.session_state.cleaned_df = sample_df
                st.success(f"✅ Loaded {len(sample_df)} sales records!")
                st.balloons()
            except FileNotFoundError:
                st.error("Sample data file not found.")
    
    with col3:
        if st.button("📚 View Examples Guide", help="Open comprehensive examples documentation", key="main_view_examples"):
            st.info("📖 Check out the **Examples Guide** below for detailed tutorials!")
    
    st.divider()
    
    # Status and Quick Actions
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Current Status")
        if st.session_state.cleaned_df is not None:
            df = st.session_state.cleaned_df
            st.success(f"✅ Data loaded: {len(df)} rows × {len(df.columns)} columns")
            
            # Show quick data preview
            with st.expander("🔍 Data Preview", expanded=False):
                st.dataframe(df.head())
                
            # Quick stats
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            cat_cols = df.select_dtypes(include=['object']).columns
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Numeric Columns", len(numeric_cols))
            with col_b:
                st.metric("Text Columns", len(cat_cols))
            with col_c:
                st.metric("Missing Values", df.isnull().sum().sum())
        else:
            st.info("📝 No data loaded yet")
            st.markdown("**Get started by:**")
            st.markdown("1. Loading sample data above, or")
            st.markdown("2. Going to **Data Cleaning** tab to upload your CSV")
    
    with col2:
        st.subheader("🎯 What You Can Do")
        st.markdown("""
        **🧹 Data Cleaning**: Upload CSV files, handle missing values, remove duplicates
        
        **📊 EDA (Exploratory Data Analysis)**: Ask questions about your data in natural language
        
        **💻 Notebook**: Write Python/PySpark code with pre-loaded libraries
        
        **🔄 ETL Assistant**: Create data transformation pipelines
        
        **📚 Resource Hub**: Search for coding guides and examples
        
        **🤖 Prompt Builder**: Create custom prompts for data analysis
        """)
    
    # Examples Guide
    st.subheader("📖 Examples & Tutorials")
    
    with st.expander("🎯 Quick Start Examples", expanded=True):
        st.markdown("""
        ### 1. **Employee Analysis Example**
        1. Click "Load Sample Employee Data" above
        2. Go to **EDA** tab and ask: "Show distribution of salary"
        3. Try: "Compare salary by department" 
        4. In **Notebook** tab, run: `df.groupby('Department')['Salary'].mean()`
        
        ### 2. **Sales Analysis Example**  
        1. Click "Load Sample Sales Data" above
        2. Go to **EDA** tab and ask: "Show correlation matrix"
        3. Try: "Find outliers in revenue"
        4. In **Notebook** tab, analyze profit margins
        
        ### 3. **Data Cleaning Workflow**
        1. Go to **Data Cleaning** tab
        2. Upload your own CSV file
        3. Follow guided cleaning steps
        4. Use cleaned data in EDA and Notebook modules
        """)
    
    with st.expander("🔥 Advanced Examples", expanded=False):
        st.markdown("""
        ### Notebook Module - Advanced Analysis
        ```python
        # Performance vs Experience Analysis
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Load data (automatically available as 'df')
        correlation = df['Performance_Score'].corr(df['Years_Experience'])
        print(f"Correlation: {correlation:.3f}")
        
        # Visualize
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='Years_Experience', y='Performance_Score', hue='Department')
        plt.title('Performance vs Experience by Department')
        plt.show()
        ```
        
        ### PySpark Example
        ```python
        # Convert to Spark DataFrame
        spark_df = spark.createDataFrame(df)
        spark_df.createOrReplaceTempView("employees")
        
        # SQL analysis
        result = spark.sql(\"\"\"
            SELECT Department, 
                   AVG(Salary) as avg_salary,
                   COUNT(*) as count
            FROM employees 
            GROUP BY Department
            ORDER BY avg_salary DESC
        \"\"\")
        result.show()
        ```
        
        ### EDA Natural Language Queries
        - "Show distribution of salary"
        - "Compare performance by department"  
        - "Find outliers in years of experience"
        - "Show correlation between age and salary"
        - "Create scatter plot of experience vs performance"
        """)
    
    with st.expander("🛠️ Module-Specific Examples", expanded=False):
        st.markdown("""
        ### 🧹 Data Cleaning Examples
        - **Remove duplicates**: Automatically detect and remove duplicate rows
        - **Handle missing values**: Choose from mean/median imputation or removal
        - **Data type conversion**: Convert strings to dates, numbers, etc.
        - **Outlier detection**: Identify and handle extreme values
        
        ### 📊 EDA Natural Language Examples
        - **"Show distribution of [column]"** → Histogram + statistics
        - **"Compare [numeric] by [category]"** → Box plots + summary tables  
        - **"Show correlation matrix"** → Heatmap of correlations
        - **"Find outliers in [column]"** → Outlier detection + visualization
        - **"Show summary"** → Complete dataset overview
        
        ### 💻 Notebook Code Examples
        - **Data loading**: `df = pd.read_csv('file.csv')`
        - **Quick analysis**: `df.describe()`, `df.info()`
        - **Visualizations**: Matplotlib, Seaborn, Plotly examples
        - **PySpark operations**: DataFrame transformations, SQL queries
        - **Machine learning**: Scikit-learn integration examples
        
        ### 🔄 ETL Examples
        - **Data transformation**: Clean, filter, aggregate data
        - **Join operations**: Combine multiple datasets
        - **Export options**: CSV, Excel, database storage
        - **Pipeline automation**: Repeatable ETL workflows
        """)
    
    # Tips section
    st.subheader("💡 Pro Tips")
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **🎯 Getting Started:**
        - Start with sample data to learn the interface
        - Use EDA for quick insights before coding
        - Check Resource Hub for coding help
        """)
    
    with tips_col2:
        st.markdown("""
        **⚡ Advanced Usage:**
        - Combine modules for complete workflows  
        - Export results between modules
        - Use PySpark for large datasets
        """)
    
    # Footer
    st.divider()
    st.markdown("*💡 **Need help?** Check the Resource Hub tab for guides, or ask questions in the Notebook assistant!*")

with tab2:
    st.header("Data Cleaning")
    clean_data()

with tab3:
    st.header("Exploratory Data Analysis (EDA)")
    perform_eda()

with tab4:
    st.header("Notebook")
    run_notebook()

with tab5:
    st.header("ETL Assistant")
    run_etl_agent()

with tab6:
    st.header("Resource Hub")
    query = st.text_input(
        "Search for guides (e.g., 'pandas groupby')",
        help="Search API-fetched docs and snippets.",
    )
    if query:
        results = search_knowledge_base(query)
        for result in results:
            with st.expander(result['title']):
                st.write(result['content'])
                st.code(result['code'], language='python')

with tab7:
    st.header("Prompt Builder")
    build_prompt()

