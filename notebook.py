import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from io import BytesIO, StringIO
import sys
import re
from openai_agent import run_agent

def run_notebook():
    st.header("Notebook Module")
    st.info(
        "This module simulates a Databricks/Jupyter notebook. Write Python, PySpark, or SQL code with pre-imported libraries (pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns, sqlite3, SparkSession as spark). Use 'df' for cleaned data if available. Run code, view outputs, get suggestions, or ask the coding assistant for help.",
        icon="ℹ️"
    )

    # Pre-import major libraries
    exec_globals = {
        'pd': pd,
        'np': np,
        'plt': plt,
        'sns': sns,
        'sqlite3': sqlite3,
        'col': col,
        'st': st,  # Allow Streamlit commands for advanced users
    }

    # Initialize SparkSession for PySpark
    try:
        spark = SparkSession.builder.appName("StreamlitNotebook").config("spark.driver.memory", "2g").getOrCreate()
        exec_globals['spark'] = spark
    except Exception as e:
        st.warning(f"PySpark initialization failed. PySpark code may not work. Error: {str(e)}")
        exec_globals['spark'] = None

    # Load cleaned data if available
    if 'cleaned_df' in st.session_state and st.session_state.cleaned_df is not None:
        exec_globals['df'] = st.session_state.cleaned_df
        st.info("Pre-loaded 'df' from Data Cleaning module. Use it directly in your code.")

    # Code input with IntelliSense-like suggestions
    st.subheader("Code Cell")
    code_suggestions = get_code_suggestions(exec_globals)
    selected_suggestion = st.selectbox(
        "Select a code snippet to insert (optional)",
        ["None"] + [s['text'] for s in code_suggestions],
        help="Choose a snippet to pre-fill the code area with common operations based on your data or context."
    )
    if selected_suggestion != "None":
        initial_code = next((s['code'] for s in code_suggestions if s['text'] == selected_suggestion), "")
    else:
        initial_code = ""
    
    code = st.text_area(
        "Enter Python, PySpark, or SQL code",
        value=initial_code,
        height=200,
        help="Write code here. For SQL, use sqlite3.connect('app.db') to query the app's database (e.g., data_dictionary table). Suggestions and error fixes appear after running."
    )

    # Copilot-like chatbot assistant
    st.subheader("Coding Assistant")
    assistant_query = st.text_input(
        "Ask for coding help (e.g., 'How do I group by a column?', 'Explain this error')",
        help="Type a question or describe your coding need. The assistant provides code snippets or explanations based on your input or current code."
    )
    if assistant_query:
        try:
            response = get_assistant_response(assistant_query, code, exec_globals)
            st.write(response['text'])
            if 'code' in response:
                st.code(response['code'], language='python')
        except Exception as e:
            st.error(f"Assistant error: {str(e)}")

    # Run code
    if st.button("Run Code", help="Execute the code and view outputs, suggestions, or error fixes."):
        if code:
            try:
                # Redirect stdout for prints
                old_stdout = sys.stdout
                sys.stdout = mystdout = StringIO()

                # Execute code
                exec(code, exec_globals)

                # Restore stdout
                sys.stdout = old_stdout
                output_text = mystdout.getvalue()

                # Display console output
                if output_text:
                    st.text("Console Output:")
                    st.text(output_text)

                # Display DataFrames or Series
                for var_name, var_value in list(exec_globals.items()):
                    if isinstance(var_value, pd.DataFrame):
                        st.write(f"DataFrame '{var_name}':")
                        st.dataframe(var_value.head(10))  # Limit to 10 rows
                        # Export options
                        st.download_button(
                            label=f"Download {var_name} as CSV",
                            data=var_value.to_csv(index=False),
                            file_name=f"{var_name}.csv",
                            mime="text/csv"
                        )
                        excel_output = BytesIO()
                        with pd.ExcelWriter(excel_output, engine='openpyxl') as writer:
                            var_value.to_excel(writer, index=False)
                        st.download_button(
                            label=f"Download {var_name} as Excel",
                            data=excel_output.getvalue(),
                            file_name=f"{var_name}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    elif isinstance(var_value, pd.Series):
                        st.write(f"Series '{var_name}':")
                        st.write(var_value.head(10))

                # Display plots
                if plt.get_fignums():
                    st.pyplot(plt.gcf())
                    plt.clf()

                # Next-step recommendations
                st.subheader("Next Steps")
                suggestions = get_next_step_suggestions(code, exec_globals)
                for suggestion in suggestions:
                    st.write(suggestion['text'])
                    st.code(suggestion['code'], language='python')

            except Exception as e:
                st.error(f"Error executing code: {str(e)}")
                st.subheader("Fix Suggestions")
                fix_suggestions = get_error_fix_suggestions(str(e), code)
                for fix in fix_suggestions:
                    st.write(fix['text'])
                    if 'code' in fix:
                        st.code(fix['code'], language='python')
        else:
            st.warning("Please enter code to run.")

def get_code_suggestions(exec_globals):
    suggestions = []
    
    # Base suggestions with comprehensive examples
    suggestions.extend([
        {'text': "Load sample employee data", 'code': "# Load sample employee data\ndf = pd.read_csv('sample_data.csv')\nprint(f'Loaded {len(df)} employees')\ndf.head()"},
        {'text': "Load sample sales data", 'code': "# Load sample sales data\nsales_df = pd.read_csv('sample_sales_data.csv')\nprint(f'Loaded {len(sales_df)} sales records')\nsales_df.head()"},
        {'text': "Data overview and statistics", 'code': "# Get comprehensive data overview\nprint('Dataset shape:', df.shape)\nprint('\\nColumn info:')\nprint(df.info())\nprint('\\nSummary statistics:')\ndf.describe()"},
        {'text': "Data quality check", 'code': "# Check for missing values and duplicates\nprint('Missing values per column:')\nprint(df.isnull().sum())\nprint(f'\\nDuplicate rows: {df.duplicated().sum()}')\nprint(f'Unique values per column:')\nfor col in df.columns:\n    print(f'{col}: {df[col].nunique()}')"},
        {'text': "Basic data visualization", 'code': "# Create basic visualizations\nfig, axes = plt.subplots(2, 2, figsize=(12, 10))\n\n# Histogram of first numeric column\nnumeric_cols = df.select_dtypes(include=['int64', 'float64']).columns\nif len(numeric_cols) > 0:\n    df[numeric_cols[0]].hist(ax=axes[0,0], bins=20)\n    axes[0,0].set_title(f'Distribution of {numeric_cols[0]}')\n\n# Box plot if we have categorical and numeric columns\ncat_cols = df.select_dtypes(include=['object']).columns\nif len(cat_cols) > 0 and len(numeric_cols) > 0:\n    df.boxplot(column=numeric_cols[0], by=cat_cols[0], ax=axes[0,1])\n    axes[0,1].set_title(f'{numeric_cols[0]} by {cat_cols[0]}')\n\n# Correlation heatmap if multiple numeric columns\nif len(numeric_cols) > 1:\n    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=axes[1,0])\n    axes[1,0].set_title('Correlation Matrix')\n\n# Value counts for first categorical column\nif len(cat_cols) > 0:\n    df[cat_cols[0]].value_counts().plot(kind='bar', ax=axes[1,1])\n    axes[1,1].set_title(f'Count of {cat_cols[0]}')\n    axes[1,1].tick_params(axis='x', rotation=45)\n\nplt.tight_layout()\nplt.show()"},
        {'text': "SQL query on app database", 'code': "# Query the app's internal database\nconn = sqlite3.connect('app.db')\nresult = pd.read_sql_query('SELECT * FROM data_dictionary LIMIT 10', conn)\nconn.close()\nprint(f'Found {len(result)} records in data_dictionary')\nresult"}
    ])

    # Context-aware suggestions based on loaded data
    if 'df' in exec_globals and isinstance(exec_globals['df'], pd.DataFrame):
        df = exec_globals['df']
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        cat_cols = df.select_dtypes(include=['object']).columns
        
        if not numeric_cols.empty:
            col = numeric_cols[0]
            suggestions.extend([
                {'text': f"Advanced analysis of {col}", 'code': f"# Detailed analysis of {col}\nprint(f'{col} statistics:')\nprint(f'Mean: ' + str(df['{col}'].mean().round(2)))\nprint(f'Median: ' + str(df['{col}'].median().round(2)))\nprint(f'Std Dev: ' + str(df['{col}'].std().round(2)))\nprint(f'Min: ' + str(df['{col}'].min()))\nprint(f'Max: ' + str(df['{col}'].max()))\n\n# Quartiles and outliers\nQ1 = df['{col}'].quantile(0.25)\nQ3 = df['{col}'].quantile(0.75)\nIQR = Q3 - Q1\noutliers = df[(df['{col}'] < Q1 - 1.5*IQR) | (df['{col}'] > Q3 + 1.5*IQR)]\nprint(f'Outliers detected: ' + str(len(outliers)))\n\n# Visualization\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))\nsns.histplot(df['{col}'], kde=True, ax=ax1)\nax1.set_title(f'Distribution of {col}')\nsns.boxplot(y=df['{col}'], ax=ax2)\nax2.set_title(f'Box Plot of {col}')\nplt.show()"},
                {'text': "Group analysis and aggregation", 'code': f"# Group analysis example\nif len(df.select_dtypes(include=['object']).columns) > 0:\n    group_col = df.select_dtypes(include=['object']).columns[0]\n    grouped = df.groupby(group_col)['{col}'].agg(['count', 'mean', 'median', 'std']).round(2)\n    print(f'{col} statistics by category:')\n    print(grouped)\n    \n    # Visualization\n    plt.figure(figsize=(10, 6))\n    df.groupby(group_col)['{col}'].mean().plot(kind='bar')\n    plt.title(f'Average {col} by Category')\n    plt.xticks(rotation=45)\n    plt.ylabel(f'Average {col}')\n    plt.show()"},
            ])
        
        if len(cat_cols) > 0:
            cat_col = cat_cols[0]
            suggestions.append({
                'text': f"Categorical analysis of {cat_col}",
                'code': f"# Analyze {cat_col} distribution\nvalue_counts = df['{cat_col}'].value_counts()\nprint(f'{cat_col} distribution:')\nprint(value_counts)\nprint(f'\\nPercentage distribution:')\nprint((value_counts / len(df) * 100).round(2))\n\n# Visualization\nfig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))\n\n# Bar chart\nvalue_counts.plot(kind='bar', ax=ax1)\nax1.set_title(f'Count of {cat_col}')\nax1.tick_params(axis='x', rotation=45)\n\n# Pie chart\nvalue_counts.plot(kind='pie', ax=ax2, autopct='%1.1f%%')\nax2.set_title(f'Distribution of {cat_col}')\nax2.set_ylabel('')\n\nplt.tight_layout()\nplt.show()"
            })

    # PySpark suggestions
    if 'spark' in exec_globals and exec_globals['spark'] is not None:
        suggestions.extend([
            {'text': "PySpark DataFrame operations", 'code': "# Convert pandas DataFrame to Spark DataFrame\nif 'df' in locals():\n    spark_df = spark.createDataFrame(df)\n    print(f'Created Spark DataFrame with {spark_df.count()} rows')\n    spark_df.printSchema()\n    spark_df.show(5)\nelse:\n    # Load data directly with Spark\n    spark_df = spark.read.csv('sample_data.csv', header=True, inferSchema=True)\n    spark_df.show(5)"},
            {'text': "PySpark SQL example", 'code': "# SQL operations with Spark\nif 'spark_df' in locals():\n    spark_df.createOrReplaceTempView('data_table')\n    \n    # Example SQL queries\n    result1 = spark.sql('SELECT * FROM data_table LIMIT 10')\n    result1.show()\n    \n    # Aggregation example\n    if 'Department' in [col.name for col in spark_df.schema]:\n        result2 = spark.sql('''\n            SELECT Department, \n                   COUNT(*) as employee_count,\n                   AVG(Salary) as avg_salary\n            FROM data_table \n            GROUP BY Department \n            ORDER BY avg_salary DESC\n        ''')\n        result2.show()"}
        ])

    return suggestions[:8]  # Show more suggestions for better examples

def get_next_step_suggestions(code, exec_globals):
    suggestions = []
    lower_code = code.lower()

    # Data loading
    if 'read_csv' in lower_code or 'read.csv' in lower_code:
        suggestions.append({
            'text': "Explore the loaded data with summary statistics.",
            'code': "df.describe()"
        })
        suggestions.append({
            'text': "Visualize a column's distribution.",
            'code': "sns.histplot(df['your_column'])"
        })

    # DataFrame operations
    if 'df' in exec_globals and isinstance(exec_globals['df'], pd.DataFrame):
        numeric_cols = exec_globals['df'].select_dtypes(include=['float64', 'int64']).columns
        if not numeric_cols.empty:
            col = numeric_cols[0]
            suggestions.append({
                'text': f"Aggregate data by {col}.",
                'code': f"df.groupby('{col}').agg({{ 'another_column': 'sum' }})"
            })
            suggestions.append({
                'text': "Create a correlation heatmap.",
                'code': "sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')"
            })

    # PySpark
    if 'spark' in lower_code:
        suggestions.append({
            'text': "Join another PySpark DataFrame.",
            'code': "df1.join(df2, 'id', 'inner')"
        })

    # SQL
    if 'select' in lower_code or 'from' in lower_code:
        suggestions.append({
            'text': "Add a GROUP BY clause to your SQL query.",
            'code': "SELECT column, COUNT(*) FROM table GROUP BY column"
        })

    # Default
    if not suggestions:
        suggestions.append({
            'text': "Try a simple visualization.",
            'code': "plt.bar(df['x'], df['y'])\nplt.show()"
        })

    return suggestions[:3]

def get_error_fix_suggestions(error_msg, code):
    suggestions = []
    lower_error = error_msg.lower()

    if 'nameerror' in lower_error:
        try:
            missing_name = error_msg.split("'")[1] if "'" in error_msg else "variable"
        except IndexError:
            missing_name = "variable"
        suggestions.append({
            'text': f"'{missing_name}' not defined. Check spelling or define it.",
            'code': f"{missing_name} = your_value" if missing_name not in ['pandas', 'numpy', 'matplotlib', 'seaborn'] else f"import {missing_name}"
        })

    if 'keyerror' in lower_error:
        try:
            missing_key = error_msg.split("'")[1] if "'" in error_msg else "column"
        except IndexError:
            missing_key = "column"
        suggestions.append({
            'text': f"Column '{missing_key}' not found. List available columns.",
            'code': "df.columns"
        })

    if 'syntaxerror' in lower_error:
        suggestions.append({
            'text': "Syntax error. Check indentation, parentheses, or quotes.",
            'code': "# Example: df = pd.read_csv('file.csv')"
        })

    if 'importerror' in lower_error:
        try:
            missing_module = error_msg.split("'")[1] if "'" in error_msg else "module"
        except IndexError:
            missing_module = "module"
        suggestions.append({
            'text': f"Module '{missing_module}' not imported.",
            'code': f"import {missing_module}"
        })

    if 'typeerror' in lower_error:
        suggestions.append({
            'text': "Type mismatch. Check data types of columns.",
            'code': "df.dtypes"
        })

    if 'valueerror' in lower_error:
        suggestions.append({
            'text': "Invalid value. Verify input formats.",
            'code': "df['column'] = pd.to_numeric(df['column'], errors='coerce')"
        })

    if 'sqlite3' in lower_error or 'operationalerror' in lower_error:
        suggestions.append({
            'text': "SQL error. Verify table name or connection.",
            'code': "conn = sqlite3.connect('app.db')\ncursor = conn.cursor()\ncursor.execute('SELECT * FROM data_dictionary')\nresults = cursor.fetchall()"
        })

    suggestions.append({
        'text': "Inspect your DataFrame for issues.",
        'code': "df.info()"
    })

    return suggestions[:3]

def get_assistant_response(query, code, exec_globals):

    query = query.lower()
    response = {'text': "Here's how you can proceed:"}

    # Common coding queries
    if 'group by' in query:
        if 'df' in exec_globals and isinstance(exec_globals['df'], pd.DataFrame):
            col = exec_globals['df'].columns[0]
            response['code'] = f"df.groupby('{col}').sum()"
            response['text'] = f"Group your DataFrame by a column like '{col}' and aggregate."
        else:
            response['code'] = "df.groupby('column').sum()"
            response['text'] = "Group by requires a DataFrame. Load one first."

    elif 'plot' in query or 'visualize' in query:
        if 'df' in exec_globals and isinstance(exec_globals['df'], pd.DataFrame):
            numeric_cols = exec_globals['df'].select_dtypes(include=['float64', 'int64']).columns
            if numeric_cols.empty:
                response['text'] = "No numeric columns for plotting. Try a different dataset."
            else:
                col = numeric_cols[0]
                response['code'] = f"sns.histplot(df['{col}'])"
                response['text'] = f"Create a histogram for '{col}'."
        else:
            response['code'] = "plt.plot(df['x'], df['y'])\nplt.show()"
            response['text'] = "Load a DataFrame to plot data."

    elif 'sql query' in query or 'select' in query:
        response['code'] = "conn = sqlite3.connect('app.db')\nresult = pd.read_sql_query('SELECT * FROM data_dictionary', conn)\nconn.close()\nresult"
        response['text'] = "Run a SQL query on the app's database (e.g., data_dictionary table)."

    elif 'error' in query and code:
        # Re-run error detection
        try:
            exec(code, exec_globals)
        except Exception as e:
            fixes = get_error_fix_suggestions(str(e), code)
            response['text'] = f"Error detected: {str(e)}. Try these fixes:"
            response['code'] = fixes[0].get('code', '')
    
    else:
        response['text'] = "Not sure what you need. Try asking about grouping, plotting, or SQL queries."
        response['code'] = "df.info()"

    return response