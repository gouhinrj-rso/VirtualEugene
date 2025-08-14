# Databricks notebook source
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

def run_notebook():
    code = st.text_area("Enter Python/PySpark code", height=200)
    if st.button("Run Code"):
        try:
            # Create a buffer for capturing output
            output = BytesIO()
            exec_globals = {'pd': pd, 'plt': plt}
            exec(code, exec_globals)
            
            # If a DataFrame is created, display and offer export
            for var in exec_globals:
                if isinstance(exec_globals[var], pd.DataFrame):
                    df = exec_globals[var]
                    st.write("DataFrame Output:", df)
                    st.download_button(
                        label="Download as CSV",
                        data=df.to_csv(index=False),
                        file_name="output.csv",
                        mime="text/csv"
                    )
                    st.download_button(
                        label="Download as Excel",
                        data=df.to_excel(index=False, engine='openpyxl'),
                        file_name="output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            # Display plots if created
            if plt.get_fignums():
                st.pyplot(plt)
                plt.clf()
        except Exception as e:
            st.error(f"Error: {str(e)}")