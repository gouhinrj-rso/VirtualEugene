# Databricks notebook source
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

def perform_eda():
    if st.session_state.cleaned_df is not None:
        df = st.session_state.cleaned_df
        st.write("Using Cleaned Data:", df.head())
    else:
        uploaded_file = st.file_uploader("Upload CSV for EDA", type="csv")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.session_state.cleaned_df = df
        else:
            st.warning("Please upload a CSV or clean data first in the Data Cleaning module.")
            return
    
    # Ask questions
    question = st.text_input("Ask a question about your data (e.g., 'Show distribution of sales')")
    if question:
        try:
            # Simple parsing for common questions
            if "distribution" in question.lower():
                col = st.selectbox("Select column for distribution", df.columns)
                plt.figure()
                sns.histplot(df[col])
                st.pyplot(plt)
                plt.clf()
                st.write(f"Suggested next step: Check correlations with {col}")
                st.code(f"df.corr()['{col}']", language='python')
            
            elif "correlation" in question.lower():
                plt.figure()
                sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
                st.pyplot(plt)
                plt.clf()
                st.write("Suggested next step: Visualize a scatter plot for related columns")
                st.code(f"plt.scatter(df['col1'], df['col2'])", language='python')
            
            # Export DataFrame
            st.download_button(
                label="Download Data as CSV",
                data=df.to_csv(index=False),
                file_name="eda_data.csv",
                mime="text/csv"
            )
            st.download_button(
                label="Download Data as Excel",
                data=df.to_excel(index=False, engine='openpyxl'),
                file_name="eda_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error: {str(e)}")