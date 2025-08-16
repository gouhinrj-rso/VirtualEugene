#1548

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

def perform_eda():
    if st.session_state.cleaned_df is not None:
        df = st.session_state.cleaned_df
        st.write("Using Cleaned Data:", df.head(10))  # Limit preview to 10 rows
    else:
        uploaded_file = st.file_uploader("Upload CSV for EDA", type="csv")
        if uploaded_file:
            # Check file size (limit to 10MB)
            if uploaded_file.size > 10 * 1024 * 1024:
                st.warning("File is larger than 10MB. This may slow down processing. Consider uploading a smaller dataset.")
                return
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8', encoding_errors='ignore')
                st.session_state.cleaned_df = df
                st.write("Uploaded Data Preview:", df.head(10))
            except Exception as e:
                st.error(f"Error uploading CSV: {str(e)}")
                return
        else:
            st.warning("Please upload a CSV or clean data first in the Data Cleaning module.")
            return

    # Validate DataFrame
    if df.empty:
        st.error("The DataFrame is empty. Please upload a valid dataset.")
        return
    if len(df) > 100000:
        st.warning("Large dataset detected (>100,000 rows). Visualizations and exports may be slow.")

    # Ask questions
    st.subheader("Ask About Your Data")
    question = st.text_input("Ask a question (e.g., 'Show distribution of sales')")
    if question:
        try:
            # Expanded question parsing
            if "distribution" in question.lower():
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                if not numeric_cols.empty:
                    col = st.selectbox("Select column for distribution", numeric_cols)
                    plt.figure(figsize=(8, 6))
                    sns.histplot(df[col].dropna(), kde=True)
                    st.pyplot(plt)
                    plt.clf()
                    st.write(f"Suggested next step: Check correlations with {col}")
                    st.code(f"df.corr(numeric_only=True)['{col}']", language='python')
                else:
                    st.warning("No numeric columns available for distribution plot.")
            
            elif "correlation" in question.lower():
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                if len(numeric_cols) >= 2:
                    plt.figure(figsize=(10, 8))
                    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
                    st.pyplot(plt)
                    plt.clf()
                    st.write("Suggested next step: Visualize a scatter plot for correlated columns")
                    col1, col2 = numeric_cols[:2]  # Pick first two numeric columns
                    st.code(f"plt.scatter(df['{col1}'], df['{col2}'])", language='python')
                else:
                    st.warning("Need at least two numeric columns for correlation analysis.")
            
            elif "mean" in question.lower() or "average" in question.lower():
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                if not numeric_cols.empty:
                    col = st.selectbox("Select column for mean", numeric_cols)
                    mean_val = df[col].mean()
                    st.write(f"Mean of {col}: {mean_val:.2f}")
                    st.write("Suggested next step: Visualize the distribution of this column")
                    st.code(f"sns.histplot(df['{col}'])", language='python')
                else:
                    st.warning("No numeric columns available for mean calculation.")
            
            elif "scatter" in question.lower():
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                if len(numeric_cols) >= 2:
                    col1 = st.selectbox("Select X column for scatter plot", numeric_cols)
                    col2 = st.selectbox("Select Y column for scatter plot", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
                    plt.figure(figsize=(8, 6))
                    sns.scatterplot(x=df[col1], y=df[col2])
                    st.pyplot(plt)
                    plt.clf()
                    st.write("Suggested next step: Check correlation between these columns")
                    st.code(f"df[['{col1}', '{col2}']].corr()", language='python')
                else:
                    st.warning("Need at least two numeric columns for scatter plot.")
            
            else:
                st.info("Question not recognized. Try 'distribution', 'correlation', 'mean', or 'scatter'.")
                st.write("Suggested next step: View summary statistics")
                st.code("df.describe()", language='python')
                st.write(df.describe())
            
            # Export DataFrame
            st.subheader("Export Data")
            st.download_button(
                label="Download Data as CSV",
                data=df.to_csv(index=False),
                file_name="eda_data.csv",
                mime="text/csv"
            )
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button(
                label="Download Data as Excel",
                data=output.getvalue(),
                file_name="eda_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error processing question: {str(e)}")
